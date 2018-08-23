"""scraper.py
"""
import re
import requests
from bs4 import BeautifulSoup

DEFAULT_HTML_PARSER = 'html.parser'

INCOME_STATEMENT_URL = 'https://www.marketwatch.com/investing/stock/{}/financials'
BALANCE_SHEET_URL = 'https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet'
CASH_FLOW_URL = 'https://www.marketwatch.com/investing/stock/{}/financials/cash-flow'

EPS_TTM_URL = 'https://www.gurufocus.com/financials/{}'
EPS_QOQ_URL = 'https://ycharts.com/companies/{}/eps'
REVENUE_QOQ_URL = 'https://ycharts.com/companies/{}/revenues'
EARNINGS_GROWTH_URL = 'https://www.nasdaq.com/symbol/{}/earnings-growth'
PE_RATIO_URL = 'https://www.gurufocus.com/term/pe/{}/PE-Ratio'

SALES_GROWTH_DIV = 'ratio_SalesNet1YrGrowth'
EPS_GROWTH_DIV = 'ratio_Eps1YrAnnualGrowth'
EQUITY_GROWTH_DIV = 'ratio_TotalShareholdersEquityToTotalAssets'
FREE_CASH_FLOW_GROWTH_DIV = 'ratio_FreeCashFlowGrowth'


class Scraper(object):
    def __init__(self):
        self.cache = {}

    def __to_float(self, s):
        """
        Converts a string s into a float.
        :param s: The string to be converted into a float
        :return: A float
        """
        import re
        nums_only = re.sub(r'[^0-9.BMK]', '', s)
        if nums_only == '':
            nums_only = '0'
        return float(nums_only)

    def __fix_time_prefix(self, time_str):
        splitted = time_str.split(' ')

        # Set the month to the three character abbreviation
        splitted[0] = splitted[0][:3]
        return ' '.join(splitted)

    def __fix_dollar_prefix(self, amt_str):
        # If amt_str is a number, just return the float representation
        try:
            return self.__to_float(amt_str)
        except ValueError:
            dollars = self.__to_float(amt_str[:-1])
            prefix = amt_str[-1]

            if prefix == 'B':
                dollars *= 1000000000
            elif prefix == 'M':
                dollars *= 1000000
            elif prefix == 'K':
                dollars *= 1000
            return dollars

    def __get_scrape_soup(self, url):
        # Grab web page if it is in cache
        if url in self.cache:
            web_page = self.cache[url]
        else:
            web_page = requests.get(url)
            self.cache[url] = web_page
        return BeautifulSoup(web_page.text, DEFAULT_HTML_PARSER)

    def __grab_growth_rates(self, local_soup, div_id):
        """
        Scrapes the growth rate percentages from the financial data table
        on MarketWatch.com for a specified stock

        :param div_id: The id of the div to extract growth information from
        :return: An array of length 5, with the last four elements containing growth percentages or
                 None if an error occurred in fetching the div elements
        """

        try:
            statistics = local_soup.find('tr', id=div_id).find_all('td', class_='valueCell')
            return [self.__to_float(td.text) for td in statistics]
        except Exception:
            return [0] * 5

    def get_stock_name(self, ticker):
        """
        Retrieves a stock's company name with a given ticker.
        :param ticker: str The ticker of the stock
        :return: str The name of the company
        """
        url = INCOME_STATEMENT_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        company_name = soup.find('h1', id='instrumentname').text
        return company_name

    def get_quarterly_financials(self, ticker, kind):
        url = None
        if kind == 'eps':
            url = EPS_QOQ_URL.format(ticker.upper())
        elif kind == 'revenue':
            url = REVENUE_QOQ_URL.format(ticker.upper())
        else:
            return []
        soup = self.__get_scrape_soup(url)
        table_rows = soup.find('table', class_='histDataTable').find_all('tr')
        return [{'time': self.__fix_time_prefix(row.find_all('td')[0].text.strip()),
                 'data': self.__fix_dollar_prefix(row.find_all('td')[1].text.strip())} for row in table_rows[1:]]

    def get_qoq_growth(self, ticker, kind):
        # If `kind` is incorrectly specified, just return 0.
        data_points = self.get_quarterly_financials(ticker, kind)
        if len(data_points) == 0:
            return 0
        current_value = data_points[0]['data']
        former_value = data_points[4]['data']
        if current_value >= former_value:
            return current_value / former_value - 1
        return -(1 - current_value / former_value)

    def get_sales_growth(self, ticker):
        url = INCOME_STATEMENT_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        return self.__grab_growth_rates(soup, SALES_GROWTH_DIV)

    def get_eps_growth(self, ticker):
        url = INCOME_STATEMENT_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        return self.__grab_growth_rates(soup, EPS_GROWTH_DIV)

    def get_equity_growth(self, ticker):
        url = BALANCE_SHEET_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        return self.__grab_growth_rates(soup, EQUITY_GROWTH_DIV)

    def get_free_cash_flow_growth(self, ticker):
        url = CASH_FLOW_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        return self.__grab_growth_rates(soup, FREE_CASH_FLOW_GROWTH_DIV)

    def get_eps_ttm(self, ticker):
        url = EPS_TTM_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        try:
            most_recent_ttm = soup.find('tr', onclick=re.compile(r'eps&trendline')) \
                              .find('div', class_='td_normal_pershare yesttm')

            return self.__to_float(most_recent_ttm['title'])
        except Exception as e:
            raise ValueError("Error encountered when attempting to get TTM EPS from {}: {}".format(url, e))

    def get_avg_equity_growth(self, ticker):
        equity_growth = self.get_equity_growth(ticker)
        try:
            return sum(equity_growth) / len(equity_growth)
        except Exception as e:
            raise ValueError("Error encountered when attempting to get average equity growth for {}: {}".format(ticker, e))

    def get_avg_earnings_growth(self, ticker):
        """
        Retrieves the expected average earnings growth over the next five years.
        :param ticker:
        :return:
        """
        url = EARNINGS_GROWTH_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        try:
            growth_paragraph = soup.find('span', id='quotes_content_left_textinfo').contents[0]

            # Get the estimate by cutting out the first percentage number from the first sentence.
            return self.__to_float(growth_paragraph[127:growth_paragraph.find('%')])
        except Exception as e:
            raise ValueError("Error encountered when attempting to get avg 5-year earnings estimate for {} from {}: {}".format(ticker, url, e))

    def get_recent_pe(self, ticker):
        """
        Gets the most recent P/E ratio for the a stock with the given ticker.
        :param ticker:
        :return:
        """
        url = PE_RATIO_URL.format(ticker)
        soup = self.__get_scrape_soup(url)
        try:
            most_recent_pe = soup.find('div', id='target_def_description') \
                .find('div') \
                .find('p') \
                .find_all('strong')[6].contents

            return self.__to_float(most_recent_pe[0])
        except Exception as e:
            raise ValueError("Error encountered when attempting to get the most recent P/E for {} from {}: {}".format(ticker, url, e))


if __name__ == '__main__':
    s = Scraper()
    print(s.get_stock_name('fb'))
import sys

import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('stocks.db')
c = conn.cursor()

def top_stocks():
    import json
    snp = 'snp.json'
    f = open(snp, 'r')

    lst = json.loads(f.read())
    top = []

    for company in lst:
        ticker = company['Symbol']
        print(ticker)
        big_five_matrix = get_big_five(ticker)
        if is_good_growth(big_five_matrix) or is_growing(big_five_matrix):
            top.append(ticker)

        print(top)

    print("Top stocks are: {}".format(top))

def is_growing(matrix):
    for row in matrix:
        base = 0
        for percentage in row:
            try:
                if float(percentage[:-1]) <= base:
                    return False
                base = float(percentage[:-1])
            except ValueError:
                if percentage == '!':
                    return False
                continue
    return True

def is_good_growth(matrix):
    for row in matrix:
        for percentage in row:
            try:
                if float(percentage[:-1]) < 0:
                    return False
            except ValueError:
                if percentage == '!':
                    return False
                continue

    return True


def grab_growth_rates(local_soup, div_id):
    """
    Scrapes the growth rate percentages from the financial data table
    on MarketWatch.com for a specified stock

    :param div_id: The id of the div to extract growth information from
    :return: An array of length 5, with the last four elements containing growth percentages
    """

    try:
        statistics = local_soup.find('tr', id=div_id).find_all('td', class_='valueCell')
        return [td.text for td in statistics]
    except AttributeError:
        return ['!', '!', '!', '!', '!']

def get_big_five(ticker, output=False):
    income_url = 'https://www.marketwatch.com/investing/stock/{}/financials'.format(ticker)
    income_page = requests.get(income_url)
    income_soup = BeautifulSoup(income_page.text, 'html.parser')

    balance_sheet_url = 'https://www.marketwatch.com/investing/stock/{}/financials/balance-sheet'.format(ticker)
    balance_page = requests.get(balance_sheet_url)
    balance_soup = BeautifulSoup(balance_page.text, 'html.parser')

    cash_flow_url = 'https://www.marketwatch.com/investing/stock/{}/financials/cash-flow'.format(ticker)
    cash_flow_page = requests.get(cash_flow_url)
    cash_flow_soup = BeautifulSoup(cash_flow_page.text, 'html.parser')

    # Income statement statistics
    sales_growth = grab_growth_rates(income_soup, 'ratio_SalesNet1YrGrowth')
    eps_growth = grab_growth_rates(income_soup, 'ratio_Eps1YrAnnualGrowth')

    # Balance sheet statistics
    equity_growth = grab_growth_rates(balance_soup, 'ratio_TotalShareholdersEquityToTotalAssets')

    # Cash flow statistics
    free_cash_growth = grab_growth_rates(cash_flow_soup, 'ratio_FreeCashFlowGrowth')

    if output is True:
        print("SALES:\n", sales_growth,
              "\nEPS:\n", eps_growth,
              "\nEQUITY:\n", equity_growth,
              "\nFREE CASH:\n", free_cash_growth)

    return [sales_growth, eps_growth, equity_growth, free_cash_growth]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Muse include ticker in argument parameters")
        exit(1)

    ticker = sys.argv[1]
    get_big_five(ticker, output=True)
    # top_stocks()



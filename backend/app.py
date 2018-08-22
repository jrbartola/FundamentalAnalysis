import sys
from scraper import *
from util import *

def parse_percentage_strings(percent):
    if percent == '-':
        return 0
    return float(percent[:-1].replace(',',''))

def update_stocks():
    print("Grabbing stocks")
    curr.execute("SELECT * FROM stocks")
    stocks = [s[0] for s in curr.fetchall()]

    for stock in stocks:
        print("Analyzing {}...".format(stock))
        bigfive = get_big_five(stock)
        [sales_growth, eps_growth, equity_growth, free_cash_growth] = bigfive
        try:
            sales_insertable = [(stock, year, parse_percentage_strings(sale), None) for year, sale in \
                                zip(range(2013, 2018), sales_growth)]
            curr.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", sales_insertable)
        except Exception as e:
            print("Sales insert failed. Reason: {}".format(e))
        try:
            eps_insertable = [(stock, year, parse_percentage_strings(eps), None) for year, eps in \
                                zip(range(2013, 2018), eps_growth)]
            curr.executemany("INSERT INTO eps VALUES (?, ?, ?, ?)", eps_insertable)
        except Exception as e:
            print("EPS insert failed. Reason: {}".format(e))
        try:
            equity_insertable = [(stock, year, parse_percentage_strings(equity), None) for year, equity in \
                                zip(range(2013, 2018), equity_growth)]
            curr.executemany("INSERT INTO equity VALUES (?, ?, ?, ?)", equity_insertable)
        except Exception as e:
            print("Equity failed. Reason: {}".format(e))
        try:
            cash_insertable = [(stock, year, parse_percentage_strings(cash), None) for year, cash in \
                                 zip(range(2013, 2018), free_cash_growth)]
            curr.executemany("INSERT INTO cash VALUES (?, ?, ?, ?)", cash_insertable)
        except Exception as e:
            print("Cash flow insert failed. Reason: {}".format(e))
        try:
            conn.commit()
        except Exception as e:
            print("Commit failed. Reason: {}".format(e))


def get_big_five(ticker, output=False):

    s = Scraper()
    sales_growth = s.get_sales_growth(ticker)
    eps_growth = s.get_eps_growth(ticker)
    equity_growth = s.get_equity_growth(ticker)
    free_cash_growth = s.get_free_cash_flow_growth(ticker)

    if output is True:
        print("SALES:\n", sales_growth,
              "\nEPS:\n", eps_growth,
              "\nEQUITY:\n", equity_growth,
              "\nFREE CASH:\n", free_cash_growth)

    return [sales_growth, eps_growth, equity_growth, free_cash_growth]

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print("Muse include ticker in argument parameters")
    #     exit(1)
    print("starting")
    drop_tables()
    create_tables()
    update_stocks()




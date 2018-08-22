# Contains database methods for modifying Stock data
from flaskapp import db
from scraper import Scraper
from db.models.stock import Stock
from db.models.eps import EPS
from db.models.revenues import Revenues



def get_stock(ticker=None):
    """
    Returns information about a Stock with the specified ticker. If ticker is None, then
    all stocks in the database are returned.
    :param ticker: str
    :return: Stock if found, or a list of all Stocks if ticker is unspecified.
    """
    if ticker:
        return Stock.query.filter_by(ticker=ticker).first()
    return Stock.query.all()

def update_stock_data(ticker):
    """
    Finds the stock data for a given ticker, and updates/inserts it into the database.
    :param ticker: str
    """
    scraper = Scraper()
    stock = get_stock(ticker)
    if not stock:
        name = scraper.get_stock_name(ticker)
        stock = Stock(name, ticker)
        db.session.add(stock)

    # NOTE: eps_growth only ever contains four numbers, so skip the first spot
    avg_eps_growth = sum(scraper.get_eps_growth(ticker)[1:]) / 4
    qoq_eps_growth = scraper.get_qoq_growth(ticker, 'eps')

    # NOTE: sales_growth only ever contains four numbers, so skip the first spot
    avg_sales_growth = sum(scraper.get_sales_growth(ticker)[1:]) / 4
    qoq_sales_growth = scraper.get_qoq_growth(ticker, 'revenue')
    stock.avg_eps_growth = avg_eps_growth
    stock.qoq_eps_growth = qoq_eps_growth
    stock.avg_sales_growth = avg_sales_growth
    stock.qoq_sales_growth = qoq_sales_growth
    db.session.commit()
    update_mos(ticker)

def update_mos(ticker):
    """Updates the sticker price and margin of safety for a stock with a given ticker."""
    from eval import get_margin_of_safety

    try:
        stock = get_stock(ticker)
        mos, sticker = get_margin_of_safety(ticker)
        stock.sticker = sticker
        stock.margin = mos
        db.session.commit()
    except Exception as e:
        print("Exception encountered determining Margin of Safety for {}: {}".format(ticker, e))

def update_eps_data(ticker):
    """Updates the quarterly EPS data for a stock with a given ticker."""
    from datetime import datetime

    update_stock_data(ticker)
    stock = get_stock(ticker)
    if not stock:
        # TODO
        return
    scraper = Scraper()
    datapoints = scraper.get_quarterly_financials(ticker, 'eps')
    for datum in datapoints:
        data, time = datum['data'], datetime.strptime(datum['time'], '%b %d, %Y')
        earning = EPS(ticker, time, data)
        try:
            db.session.add(earning)
        except Exception as e:
            print("Exception encountered when adding EPS for stock with ticker {}: {}".format(ticker, e))
    db.session.commit()

def get_eps_data(ticker):
    """Retrieves the quarterly EPS data for a stock with a given ticker."""
    return EPS.query.filter_by(ticker=ticker).all()

def update_revenue_data(ticker):
    """Updates the quarterly revenue data for a stock with a given ticker."""
    from datetime import datetime

    # TODO: Figure out if this is absolutely necessary
    update_stock_data(ticker)
    stock = get_stock(ticker)
    if not stock:
        # TODO
        return
    scraper = Scraper()
    datapoints = scraper.get_quarterly_financials(ticker, 'revenue')
    for datum in datapoints:
        data, time = datum['data'], datetime.strptime(datum['time'], '%b %d, %Y')
        revenue = Revenues(ticker, time, data)
        try:
            db.session.add(revenue)
        except Exception as e:
            print("Exception encountered when adding revenue for stock with ticker {}: {}".format(ticker, e))
    db.session.commit()

def get_revenue_data(ticker):
    """Retrieves the quarterly revenue data for a stock with a given ticker."""
    return Revenues.query.filter_by(ticker=ticker).all()

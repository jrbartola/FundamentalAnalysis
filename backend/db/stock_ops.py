# Contains database methods for modifying Stock data
from flaskapp import db
from sqlalchemy import exc
from scraper import Scraper
from db.models.stock import Stock
from db.revenue_ops import update_revenue_data
from db.eps_ops import update_eps_data


def get_stock(ticker=None):
    """
    Returns information about a Stock with the specified ticker. If ticker is None, then
    all stocks in the database are returned.

    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        Stock if found, or
        list[Stock] of all Stocks if ticker is unspecified.
    """
    if ticker:
        return Stock.query.filter_by(ticker=ticker).first()
    return Stock.query.all()


def add_stock(name, ticker):
    """
    Adds a stock to the database with a given name and ticker symbol.

    Args:
        name (str): The name of the stock.
        ticker (str): The stock ticker symbol.
    Returns:

    """
    try:
        stock = Stock(name, ticker)
        db.session.add(stock)
        db.session.commit()
    except exc.IntegrityError:
        # If an integrity exception occurs, rollback the session and reraise
        db.session.rollback()
        raise


def update_stock(stock):
    """
    Updates a stock in the database.

    Args:
        stock (Stock): The stock to update in the database.
    """
    try:
        db.session.add(stock)
        db.session.commit()
    except exc.IntegrityError:
        # If an integrity exception occurs, rollback the session and reraise
        db.session.rollback()
        raise


def update_stock_data(ticker):
    """
    Finds the stock data for a given ticker, and updates/inserts it into the database.
    :param ticker: str
    """
    scraper = Scraper()
    stock = get_stock(ticker)
    if not stock:
        name = scraper.get_stock_name(ticker)
        add_stock(name, ticker)
        stock = get_stock(ticker)

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
    update_stock(stock)
    update_mos(ticker)
    update_eps_data(ticker)
    update_revenue_data(ticker)


def update_mos(ticker):
    """Updates the sticker price and margin of safety for a stock with a given ticker."""
    from eval import get_margin_of_safety

    try:
        stock = get_stock(ticker)
        mos, sticker = get_margin_of_safety(ticker)
        stock.sticker = sticker
        stock.margin = mos
        update_stock(stock)
    except Exception as e:
        print("Exception encountered determining Margin of Safety for {}: {}".format(ticker, e))

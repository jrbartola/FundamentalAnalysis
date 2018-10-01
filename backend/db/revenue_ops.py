# Contains database methods for interacting with revenue data
from flaskapp import db
from sqlalchemy import exc
from scraper import Scraper
from db.models.revenues import Revenues
# from db.stock_ops import get_stock


def get_revenue_data(ticker):
    """
    Retrieves the quarterly revenue data for a stock with a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        list[Revenues]: A list of quarterly revenues for a given stock.
    """
    return Revenues.query.filter_by(ticker=ticker).all()


def add_revenue(ticker, time, revenue):
    """
    Adds a Revenues object to the database.

    Args:
        ticker (str): The stock ticker symbol.
        time (datetime.datetime): The time or date of the earnings release.
        revenue (float): The company's revenue, in dollars.
    """
    try:
        revenue = Revenues(ticker, time, revenue)
        db.session.add(revenue)
        db.session.commit()
    except exc.IntegrityError:
        # If an integrity exception occurs, rollback the session and reraise
        db.session.rollback()
        raise


def update_revenue_data(ticker):
    """
    Updates the quarterly revenue data for a stock with a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
    """
    from datetime import datetime

    scraper = Scraper()
    datapoints = scraper.get_quarterly_financials(ticker, 'revenue')
    for datum in datapoints:
        data, time = datum['data'], datetime.strptime(datum['time'], '%b %d, %Y')
        try:
            add_revenue(ticker, time, data)
        except Exception as e:
            print("Exception encountered when adding revenue for stock with ticker {}: {}".format(ticker, e))
    db.session.commit()




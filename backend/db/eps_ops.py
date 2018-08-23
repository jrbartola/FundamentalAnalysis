# Contains database methods for modifying EPS data
from flaskapp import db
from sqlalchemy import exc
from scraper import Scraper
from db.models.eps import EPS
from db.stock_ops import get_stock


def get_eps_data(ticker):
    """
    Returns EPS information about a Stock with the specified ticker.

    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        list[EPS]: A list of all company earnings.
    """
    return EPS.query.filter_by(ticker=ticker).all()


def add_eps(ticker, time, earning):
    """
    Adds an EPS object to the database.

    Args:
        ticker (str): The stock ticker symbol.
        time (datetime.datetime): The time or date of the earnings release.
        earning (float): The earnings per share, in dollars.
    """
    try:
        eps = EPS(ticker, time, earning)
        db.session.add(eps)
        db.session.commit()
    except exc.IntegrityError:
        # If an integrity exception occurs, rollback the session and reraise
        db.session.rollback()
        raise


def update_eps_data(ticker):
    """
    Updates all quarterly EPS data for a stock with a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
    """
    from datetime import datetime

    stock = get_stock(ticker)
    if not stock:
        raise RuntimeError(f"Attempted to update EPS data for non-existent stock: `{ticker}`")
    scraper = Scraper()
    datapoints = scraper.get_quarterly_financials(ticker, 'eps')
    for datum in datapoints:
        data, time = datum['data'], datetime.strptime(datum['time'], '%b %d, %Y')
        try:
            add_eps(ticker, time, data)
        except Exception as e:
            raise ValueError("Exception encountered when adding EPS for stock with ticker {}: {}".format(ticker, e))
    db.session.commit()

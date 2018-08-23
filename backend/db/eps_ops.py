# Contains database methods for modifying EPS data
from flaskapp import db
from scraper import Scraper
from db.models.eps import EPS


def get_eps_data(ticker):
    """
    Returns EPS information about a Stock with the specified ticker.

    Args:
        ticker (str): The stock ticker symbol.
    Returns:
        list[EPS]: A list of all company earnings.
    """
    return EPS.query.filter_by(ticker=ticker).all()


def add_eps(eps):
    """
    Adds an EPS object to the database.

    Args:
        eps (EPS): An object representing a company's quarterly earnings.
    """
    try:
        db.session.add(eps)
        db.session.commit()
    except Exception:
        # If an exception occurs, rollback the session and reraise
        db.session.rollback()
        raise


def update_eps_data(ticker):
    """
    Updates all quarterly EPS data for a stock with a given ticker.

    Args:
        ticker (str): The stock ticker symbol.
    """
    from datetime import datetime

    scraper = Scraper()
    datapoints = scraper.get_quarterly_financials(ticker, 'eps')
    for datum in datapoints:
        data, time = datum['data'], datetime.strptime(datum['time'], '%b %d, %Y')
        earning = EPS(ticker, time, data)
        try:
            add_eps(earning)
        except Exception as e:
            raise ValueError("Exception encountered when adding EPS for stock with ticker {}: {}".format(ticker, e))
    db.session.commit()

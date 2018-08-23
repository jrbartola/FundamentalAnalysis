# /manage.py

from flask.cli import FlaskGroup
from flaskapp import create_app, db

# Import out database models
from db.models.stock import Stock
from db.models.equity import Equity
from db.models.revenues import Revenues
from db.models.eps import EPS
from db.models.free_cash import FreeCash

import unittest

cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def get_mos():
    """Calculates the stick price and margin of safety for each stock in the database."""
    from eval import get_margin_of_safety

    stocks = Stock.query.all()
    for stock in stocks:
        print("Processing {}...".format(stock.ticker))
        try:
            mos, sticker = get_margin_of_safety(stock.ticker)
            stock.sticker = sticker
            stock.margin = mos
            db.session.commit()
        except Exception as e:
            print("Exception encountered when handling stock {}: {}".format(stock.ticker, e))

@cli.command()
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
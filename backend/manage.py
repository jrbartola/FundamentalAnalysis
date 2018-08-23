# manage.py

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
def test():
    """ Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()
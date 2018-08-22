from flaskapp import db

# Models free cash flow
class FreeCash(db.Model):
    __tablename__ = "freecash"
    ticker = db.Column(db.String(32), db.ForeignKey('stocks.ticker'), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    cash = db.Column(db.Float, nullable=True)

    def __init__(self, ticker, year, cash=None):
        self.ticker = ticker
        self.year = year
        self.cash = cash


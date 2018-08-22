from flaskapp import db

# Models equity
class Equity(db.Model):
    __tablename__ = "equity"
    ticker = db.Column(db.String(32), db.ForeignKey('stocks.ticker'), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    equity = db.Column(db.Float, nullable=True)

    def __init__(self, ticker, year, equity=None):
        self.ticker = ticker
        self.year = year
        self.equity = equity


from flaskapp import db

# Models eps
class EPS(db.Model):
    __tablename__ = "eps"
    ticker = db.Column(db.String(32), db.ForeignKey('stocks.ticker'), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    earnings = db.Column(db.Float, nullable=True)

    def __init__(self, ticker, time, earnings):
        self.ticker = ticker
        self.time = time
        self.earnings = earnings

    def to_json(self):
        return {
            'ticker': self.ticker,
            'time': self.time.timestamp(),  # Seconds since epoch
            'earnings': self.earnings
        }

from flaskapp import db

# Models sales revenue
class Revenues(db.Model):
    __tablename__ = "revenues"
    ticker = db.Column(db.String(32), db.ForeignKey('stocks.ticker'), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    revenue = db.Column(db.Float, nullable=True)

    def __init__(self, ticker, time, revenue):
        self.ticker = ticker
        self.time = time
        self.revenue = revenue

    def to_json(self):
        return {
            'ticker': self.ticker,
            'time': self.time.timestamp(),  # Seconds since epoch
            'revenue': self.revenue
        }
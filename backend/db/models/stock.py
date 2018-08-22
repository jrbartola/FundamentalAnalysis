from flaskapp import db

# Models a stock
class Stock(db.Model):
    __tablename__ = "stocks"
    ticker = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    sticker = db.Column(db.Float, nullable=True)
    margin = db.Column(db.Float, nullable=True)
    avg_eps_growth = db.Column(db.Float, nullable=True)
    qoq_eps_growth = db.Column(db.Float, nullable=True)
    avg_sales_growth = db.Column(db.Float, nullable=True)
    qoq_sales_growth = db.Column(db.Float, nullable=True)
    sales = db.relationship('Revenues', backref='stock', lazy=True)
    epss = db.relationship('EPS', backref='stock', lazy=True)
    equity = db.relationship('Equity', backref='stock', lazy=True)
    freecash = db.relationship('FreeCash', backref='stock', lazy=True)

    def __init__(self, name, ticker, sticker=None, margin=None):
        self.name = name
        self.ticker = ticker.upper()
        self.sticker = sticker
        self.margin = margin

    def to_json(self):
        return {
            'name': self.name,
            'ticker': self.ticker,
            'sticker': self.sticker,
            'margin': self.margin,
            'avgEpsGrowth': self.avg_eps_growth,
            'qoqEpsGrowth': self.qoq_eps_growth,
            'avgSalesGrowth': self.avg_sales_growth,
            'qoqSalesGrowth': self.qoq_sales_growth
        }
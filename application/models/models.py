from application import app, db
from datetime import datetime

class ConversionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_currency = db.Column(db.String(250), nullable=False)
    to_currency = db.Column(db.String(250), nullable=False)
    from_currency_rate = db.Column(db.String(250), nullable=False)
    to_currency_rate = db.Column(db.String(250), nullable=False)
    from_currency_amount = db.Column(db.String(250), nullable=False)
    result = db.Column(db.String(250), nullable=False)
    conversion_date = db.Column(db.String(250), nullable=False)
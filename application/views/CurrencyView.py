import requests
from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from sqlalchemy import text

class CurrencyView(FlaskView):
    @route('/', methods=['GET', 'POST'])
    def converter(self):
        if request.method == "POST":
            from_currency = request.form.get('from_currency')
            to_currency = request.form.get('to_currency')
            amount = request.form.get('amount')
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
            currency_rates = response.json()
            all_currency_rates = currency_rates['rates']
            from_currency_rate = all_currency_rates[from_currency]
            to_currency_rate = all_currency_rates[to_currency]
            converted_amount = round(float(amount)*to_currency_rate/from_currency_rate, 3)
            conversion_date = currency_rates['date']
            new_conversion = ConversionHistory(from_currency=from_currency,to_currency=to_currency,
                            from_currency_rate=from_currency_rate,to_currency_rate=to_currency_rate,
                            from_currency_amount=amount,result=converted_amount,conversion_date=conversion_date)
            db.session.add(new_conversion)
            db.session.commit()
            return redirect(url_for('CurrencyView:converter'))
        else:
            history = ConversionHistory.query.all()
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
            currency_rates = response.json()
            all_currency_rates = currency_rates['rates']
            currency_names = all_currency_rates.keys()
            last_converted_amount_sql = text("SELECT * FROM conversion_history ORDER BY id DESC LIMIT 1")
            last_converted_amount = db.engine.execute(last_converted_amount_sql)
            for i in last_converted_amount:
                converted_result = i
            return render_template('converter.html', currency_names=currency_names,history=history, converted_result=converted_result)
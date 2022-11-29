#!/usr/bin/env python
from flask import Flask, render_template, request

from scripts.webscraper import Converter

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    converter = Converter()
    currencies_dict = converter.get_dict_with_currencies()
    currencies = sorted(list(currencies_dict.keys()) + ["EUR"])
    if request.method == "POST":
        currency_from = request.form.get("currency_from")
        currency_to = request.form.get("currency_to")
        amount = float(request.form.get("amount"))
        result = Converter().convert_currencies(
            currencies_dict, currency_from, currency_to, amount
        )
        return render_template("index.html", currencies=currencies, result=result)
        # return f"{Converter().format_number(amount, currency_from)} is equal to {Converter().format_number(result, currency_to)}."
    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)

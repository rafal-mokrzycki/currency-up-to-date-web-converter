#!/usr/bin/env python
"""
To run type: flask --app hello run
"""
import numpy as np
from flask import Flask, flash, make_response, redirect, render_template, request, url_for

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
        return f"{Converter().format_number(amount, currency_from)} is equal to {Converter().format_number(result, currency_to)}."
    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)

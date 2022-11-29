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
    currencies = sorted(list(currencies_dict.keys()))
    if request.method == "POST":
        currency_from = request.form.get("currency_from")
        currency_to = request.form.get("currency_to")
        amount = request.form.get("amount")
        if currency_from != "EUR" and currency_to != "EUR":
            result = np.round(
                float(amount)
                * float(currencies_dict[currency_from])
                * float(currencies_dict[currency_to]),
                2,
            )
            return (
                f"{str(amount)} {currency_from} is equal to {str(result)} {currency_to}."
            )

        return redirect(url_for("home"))
    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)

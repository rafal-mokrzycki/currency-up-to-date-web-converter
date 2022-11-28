#!/usr/bin/env python
"""
To run type: flask --app hello run
"""
from flask import Flask, flash, make_response, redirect, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    currencies = ["PLN", "USD", "GPB"]
    if request.method == "POST":
        return render_template("index.html", currencies=currencies)
    return render_template("index.html", currencies=currencies)


if __name__ == "__main__":
    app.run(debug=True)

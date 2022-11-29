import logging as log
import re

import numpy as np
import requests
from bs4 import BeautifulSoup


class Converter:

    url = "https://wechselkurse-euro.de/"

    def get_dict_with_currencies(self, url=None):
        """Return a pd.DataFrame with currencies from the website 'url'."""
        if url is None:
            url = self.url
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        table_main = soup.find_all("div", class_="mb10social")
        table_additional = soup.find_all("table")
        rows_main = table_main[0].find_all("td")
        rows_additional = table_additional[0].find_all("tr") + table_additional[
            1
        ].find_all("tr")
        rows_all = rows_main + rows_additional
        dictionary = {}
        for row in rows_all:
            try:
                string = re.search(
                    '(kurz_kurz (narast|poklas|rovnako)).*[A-Z]{3}">\d+?\.\d+<', str(row)
                ).group()
                symbol = re.search("[A-Z]{3}", string).group()
                exchange_rate = re.search(">\d+?\.\d+<", string).group()[1:-1]
                dictionary[symbol] = exchange_rate
            except AttributeError:
                log.warning("String of interest not found in this line")
        return dictionary

    @staticmethod
    def convert_currencies(
        currencies_dict: dict, currency_from: str, currency_to: str, amount: int | float
    ):
        """Convert currency into another one.

        Parameters:

        currencies_dict : dict
            A dictionary with keys being currency symbol (eg. EUR, GBP, USD) and values
            being exchange rates to EUR (eg. 1.0, 3.12, 5.11).

        currency_from : str
            A currency symbol, from which the conversion will be made.

        currency_to : str
            A currency symbol, to which the conversion will be made.

        amount : int | float
            Amount of money to be converted.

        Returns:
            Result of conversion, a floating point number.

        Raises:
            ValueError if a currency symbol is not in the dictionary.
        """
        if currency_from != "EUR" and currency_to != "EUR":
            return np.round(
                float(amount)
                * float(currencies_dict[currency_from])
                * float(currencies_dict[currency_to]),
                2,
            )
        elif currency_from == "EUR" and currency_to == "EUR":
            return float(amount)
        elif currency_from == "EUR":
            return np.round(
                float(amount) * float(currencies_dict[currency_to]),
                2,
            )
        elif currency_to == "EUR":
            return np.round(
                float(amount) / float(currencies_dict[currency_from]),
                2,
            )
        else:
            raise ValueError("Wrong currency symbol.")

    @staticmethod
    def format_number(number: int | float, currency: str):
        """Formats a floating point number into string wiht a currency code,
        eg. 2.50 -> '2.50 PLN'

        Parameters:

        number : int | float
            A number to format.

        currency : str
            Currency symbol (or any other string) to format.

        Returns:
            An f-string in format: '2.50 PLN'"""
        return "{:.2f}".format(number) + f" {currency}"

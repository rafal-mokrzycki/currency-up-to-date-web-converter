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
    def convert_currencies(currencies_dict, currency_from, currency_to, amount):
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
    def format_number(number, currency):
        return "{:.2f}".format(number) + f" {currency}"

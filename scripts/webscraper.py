import logging as log
import re

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
        print(type(rows_main))
        print(type(rows_additional))
        # )
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
        print(dictionary)
        return dictionary

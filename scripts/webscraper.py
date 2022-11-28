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
        table = soup.find_all("table")
        rows = table[0].find_all("tr") + table[1].find_all("tr")
        dictionary = {}
        for row in rows:
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

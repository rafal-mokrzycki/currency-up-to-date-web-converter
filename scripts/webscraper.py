import os
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


class Converter:

    url = "https://wechselkurse-euro.de/"
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # for i in soup.find_all("tr"):
    #     if i.startswith("<td"):
    #         print("STARTS")
    #     else:
    #         print("NOT")
    #     # print(i)

    def get_table_with_currencies(self, url=None):
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
                print("String of interest not found in this line")
        return dictionary

    def render_items(self, soup_object, is_float=False):

        for line in soup_object:
            result = []
            text = line.renderContents()
            stripped_text = text.strip()
            if is_float:
                result.append(float(stripped_text))
            else:
                result.append(stripped_text[-7:-4].decode("utf-8"))
        return result


#         currencies1 = soup.find_all("td", class_="kurz_skratka center")
#         print(currencies1)
#         currencies2 = soup.find_all("td", class_="kurz_kurz pokles")
#         print(currencies2)
#         currencies3 = soup.find_all("td", class_="kurz_kurz narast") rovnako
#         print(currencies3)
#         symbols = []
#         for line1 in currencies1:
#             text = line1.renderContents()
#             number = text.strip()
#             symbols.append(number[-7:-4].decode("utf-8"))

#         rates = []
#         for line2 in currencies2:
#             text = line2.renderContents()
#             number = text.strip()
#             rates.append(float(number))
#         rates2 = []
#         for line2 in currencies3:
#             text = line2.renderContents()
#             number = text.strip()
#             rates2.append(float(number))
#         print(symbols)
#         print(rates)
#         print(len(symbols), len(rates), len(rates2))
#         # print(table)


# #     currencies = pd.DataFrame(
# #         list(zip(symbols, rates)), columns=["symbol waluty", "kurs do 1 euro"]
# #     )
# #     currencies = currencies.append(
# #         {"symbol waluty": "EUR", "kurs do 1 euro": 1.0}, ignore_index=True
# #     )

# #     URL2 = "http://kantory.pl/waluty/"
# #     page2 = requests.get(URL2)
# #     soup2 = BeautifulSoup(page2.content, "html.parser")
# #     currencies3 = soup2.find_all("tr", class_="ju12")

# #     countries = []
# #     for currency in currencies3:
# #         aux_currency = re.findall(">.*</td><td>[A-Z]{,3}</td><td>.*<", str(currency), 0)[
# #             0
# #         ]
# #         aux_currency = aux_currency.split("</td><td>")
# #         aux_currency[0] = aux_currency[0].replace("><td>", "")
# #         countries.append(aux_currency[0:3])
# #     countries = pd.DataFrame(countries, columns=["kraj", "symbol waluty", "nazwa waluty"])
# #     countries = countries.append(
# #         {"kraj": "Polska", "symbol waluty": "PLN", "nazwa waluty": "Złoty"},
# #         ignore_index=True,
# #     )

# #     corrections1 = {
# #         "AFA": "AFN",
# #         "AON": "AOA",
# #         "AZM": "AZN",
# #         "EEK": "EUR",
# #         "GHC": "GHS",
# #         "LTL": "EUR",
# #         "LVL": "EUR",
# #         "XDR": "XDR",
# #         "MZM": "MZN",
# #         "SDD": "SDG",
# #         "SRG": "SRD",
# #         "TMM": "TMT",
# #         "VEB": "VEF",
# #         "WN": "KPW",
# #         "ZWD": "ZWR",
# #     }

# #     for i in countries["symbol waluty"]:
# #         for k, v in corrections1.items():
# #             if k == i:
# #                 countries["symbol waluty"].replace(i, v, inplace=True)

# #     myrates = pd.merge(currencies, countries, how="outer", on="symbol waluty")

# #     corrections2 = [
# #         ("BMD", "Bermudy", "dolar bermudzki"),
# #         ("FKP", "Falklandy", "funt falklandzki"),
# #         ("KYD", "Kajmany", "dolar kajmański"),
# #         ("CUC", "Kuba", "peso"),
# #         ("SHP", "Wyspa Świętej Heleny", "funt Świętej Heleny"),
# #     ]

# #     for i, j in myrates.iterrows():
# #         for k in corrections2:
# #             myrates.loc[myrates["symbol waluty"] == k[0], ["kraj", "nazwa waluty"]] = (
# #                 k[1],
# #                 k[2],
# #             )
# #             myrates.loc[myrates["symbol waluty"] == "EUR", "nazwa waluty"] = "euro"

# #     myrates = myrates.dropna()

# #     def convert(self):

# #         while True:
# #             from_currency = (
# #                 input("Podaj symbol waluty, którą chcesz przeliczyć:\n")
# #             ).upper()
# #             if from_currency in self.myrates["symbol waluty"].unique():
# #                 break
# #             else:
# #                 print("Tej waluty nie ma w naszym kantorze.")
# #                 time.sleep(1)
# #         while True:
# #             to_currency = (
# #                 input("Podaj symbol waluty, na którą chcesz przeliczyć:\n")
# #             ).upper()
# #             if to_currency in self.myrates["symbol waluty"].unique():
# #                 break
# #             else:
# #                 print("Tej waluty nie ma w naszym kantorze.")
# #                 time.sleep(1)
# #         while True:
# #             try:
# #                 initial_amount = float(input("Podaj kwotę:\n"))
# #                 aux_currency = float(initial_amount) / float(
# #                     self.myrates.loc[
# #                         self.myrates["symbol waluty"] == str(from_currency),
# #                         "kurs do 1 euro",
# #                     ].iloc[0]
# #                 )
# #                 end_amount = round(
# #                     aux_currency
# #                     * float(
# #                         self.myrates.loc[
# #                             self.myrates["symbol waluty"] == str(to_currency),
# #                             "kurs do 1 euro",
# #                         ].iloc[0]
# #                     ),
# #                     2,
# #                 )
# #                 result = (
# #                     str(initial_amount)
# #                     + " "
# #                     + from_currency.upper()
# #                     + " = "
# #                     + str(end_amount)
# #                     + " "
# #                     + to_currency.upper()
#                 )
#                 break
#             except ValueError:
#                 print("Podaj liczbę, a nie ciąg znaków. Część dziesiętną oddziel kropką.")
#                 time.sleep(3)
#         return print(result)

#     def print_table(self):

#         pd.set_option("display.max_rows", None)
#         pd.set_option("display.max_columns", None)
#         return print(self.myrates)
#         time.sleep(5)

#     def save_table(self):

#         while True:
#             try:
#                 path = input(
#                     "Podaj ścieżkę folderu, w którym chcesz zapisać plik lub wciśnij 5 i ENTER, aby przejsć do opcji programu.\n"
#                 )
#                 if path == "5":
#                     break
#                 else:
#                     file = input("Podaj nazwę pliku (bez rozszerzenia):\n")
#                     filepath = str(os.path.join(path, file) + ".csv")
#                     self.myrates.to_csv(
#                         filepath, header=True, index=False, encoding="ISO-8859-2"
#                     )
#                     print("Zapisano plik.")
#                     time.sleep(1)
#                     break
#             except FileNotFoundError:
#                 print("Nie znaleziono folderu.")
#                 time.sleep(1)


# class Communicator:

#     clear = lambda: os.system("cls")
#     clear()
#     print("Witamy w przeliczniku walut!\n")
#     time.sleep(1)
#     while True:
#         try:
#             action = int(
#                 input(
#                     """
# Wpisz odpowiednią cyfrę i naciśnij ENTER:
# (1) pokaż tabelę kursów
# (2) przelicz walutę
# (3) zapisz tabelę kursów na dysku do pliku .csv
# (4) zamknij program
# """
#                 )
#             )
#             if action == 1:
#                 Converter().print_table()
#             elif action == 2:
#                 Converter().convert()
#             elif action == 3:
#                 Converter().save_table()
#             elif action == 4:
#                 print("Trwa zamykanie...")
#                 time.sleep(1)
#                 print("Zamknięto program.")
#                 break
#             else:
#                 raise ValueError()
#         except ValueError:
#             print("Podaj liczbę od 1 do 4.")
#             time.sleep(1)

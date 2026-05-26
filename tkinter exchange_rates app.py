import tkinter as tk
from tkinter import ttk
import requests

class CurrencyConventer:
    def __init__ (self, window):
        self.window = window
        self.window.title ("Konwenter walut")

        self.currencyRates = self.fetchCurrencyRates () # pobranie kursow walut i zapisanie ich w slowniku
        self.createWidgets () # utworzenie elementow UI - interfejs uzytkownika
        self.calculate () # aby pokazac od razu kursy walut

    def fetchCurrencyRates (self):
        url = "https://api.nbp.pl/api/exchangerates/tables/a/?format=json"
        response = requests.get (url)
        data = response.json ()
        currencyRates = {rate['code']: rate['mid'] for rate in data[0]["rates"]}
        return currencyRates
    
    def createWidgets (self):
        self.pln_label = ttk.Label (self.window, text = "Wprowadz kwote w PLN: ")
        self.pln_label.grid (column = 0, row = 0, padx = 10, pady = 10, sticky = "W")
        self.pln_entry = ttk.Entry (self.window)
        self.pln_entry.grid (column = 1, row = 0, padx = 10, pady = 10, sticky = "WE")
        self.pln_entry.bind ("<KeyRelease>", self.calculate) # aktualizuje wartosci przy kazdej zmianie

        #Etykiety pokazujace wartosc w walutach obcych
        self.usd_label = ttk.Label (self.window, text = "USD:")
        self.usd_label.grid (column = 0, row = 1, padx = 10, pady = 10, sticky = "W")
        self.eur_label = ttk.Label (self.window, text = "EUR:")
        self.eur_label.grid (column = 0, row = 2, padx = 10, pady = 10, sticky = "W")
        self.jpy_label = ttk.Label (self.window, text = "JPY:")
        self.jpy_label.grid (column = 0, row = 3, padx = 10, pady = 10, sticky = "W")


    def calculate (self, event = None):
        try:
            amount_pln = float (self.pln_entry.get ())
        except ValueError:
            amount_pln = 1
            self.pln_entry.delete (0, tk.END)
            self.pln_entry.insert (0, "1")

        for label, currency in [(self.usd_label, "USD"), (self.eur_label, "EUR"), (self.jpy_label, "JPY")]:
            if currency in self.currencyRates:
                value = amount_pln / self.currencyRates [currency]
                label.config (text = f"{currency} ({self.currencyRates [currency]} PLN): {value:.2f}")
            else:
                label.config (text = f"{currency} kurs nieznany: N/A")

if __name__ == "__main__":
    window = tk.Tk ()
    app = CurrencyConventer (window)
    window.mainloop ()



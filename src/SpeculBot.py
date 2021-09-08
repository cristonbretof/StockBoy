from pandas.core.frame import DataFrame
import yfinance as yf
import pandas as pd
from matplotlib import pyplot as plt
import shutil, os, time, glob
import numpy as np
from statistics import mean
import requests
from collections import deque
from threading import Event

class TickerCircularBuffer:

    def __init__(self, symbols: list, maxlen: int):
        self.deque = deque(symbols, maxlen=maxlen)

    def get_first(self):
        # Deqeue and enqeue first ticker in line
        ticker = self.deque.pop()
        self.deque.append(ticker)

        return ticker

    def rotate(self):
        ticker = self.deque.pop()
        self.deque.insert(0, ticker)


class SpeculBot:

    SELL = "SELL"
    BUY = "BUY"
    TEST = "TEST"

    def __init__(self, symbols: list, name="SpeculBot"):
        self.flag = Event()

        # API vars
        self.num_API_calls = 0
        self.stock_failures = 0

        self.name = name

        # Le maximum est arbitraire, mais je crois qu'avec plusieurs SpeculBot, il y aura des problème de rapidité
        self.tickers = TickerCircularBuffer(symbols, maxlen=100)

        # Donnée devant être transmise au contrôleur StockBoy
        self.MACD = None

    def run(self):
        while not self.flag.is_set():
            while True:
                try:
                    ticker = self.fetch_data(self.tickers.get_first())
                    history = ticker.history(period="3mo", interval="1d")[['Close', 'Open', 'High', 'Volume', 'Low']]
                    self.tickers.rotate()
                    break

                except Exception as ex:
                    if type(ex) is ValueError:
                        print("Yahoo Finance Backed Error, Attempting to Fix")
                    elif type(ex) is requests.exceptions.SSLError:
                        print("Yahoo Finance Backed Error, Attempting to Fix SSL")
                    else:
                        print("{err}".format(err=ex))

                    if self.stock_failures > 4:
                        break

                    self.stock_failures += 1

            self.macd(history)
            time.sleep(5)

    # Cette fonction pourrait être un peu plus spécifique en ce qui concerne l'information "fetché"
    def fetch_data(self, symbol: str):
        n_ticker = yf.Ticker(symbol)

        # Option de sauvegarder dans un .csv
        '''
        ticker_history.to_csv(path/to/csv)
        '''
        self.num_API_calls += 1

        return n_ticker

    def macd(self, history):
        # This list holds the closing prices of a stock
        prices = []

        # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
        for price in history['Close']:
            if price > float(2.00):  # Check that the closing price for this day is greater than $2.00
                prices.append(price)
        
        prices_df = pd.DataFrame(prices)  # Make a dataframe from the prices list

        # Calculate exponential weighted moving averages:
        day12 = prices_df.ewm(span=12, adjust=False).mean()
        day26 = prices_df.ewm(span=26, adjust=False).mean()
        macd = day12 - day26

        signal = macd.ewm(span=9, adjust=False).mean()

        condiv = macd - signal

        # Add all of our new values for the MACD to the dataframe
        history['MACD'] = macd
        history['Conv/Div'] = condiv
        history['Signal'] = signal
        # View our data
        pd.set_option("display.max_columns", None)

        print(history)
        
    def stop(self):
        self.flag.set()

    @property
    def get_name(self):
        return self.name


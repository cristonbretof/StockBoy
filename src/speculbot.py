import yfinance as yf
import time
import requests
from collections import deque
from threading import Event, Thread

from yfinance.ticker import Ticker


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

    def __init__(self, algo, symbols: list, name="SpeculBot"):
        self.flag = Event()

        # API vars
        self.num_API_calls = 0
        self.stock_failures = 0

        self.tickers = TickerCircularBuffer(symbols, maxlen=100)

        # Class properties
        self.name = name

        # Algorithm to run
        self.algo = algo

        # Donnée devant être transmise au contrôleur StockBoy
        self.latest_df = None
        self._thread = Thread(target=self.run)

    def run(self):
        while not self.flag.is_set():
            while True:
                try:
                    ticker = self.fetch_data(self.tickers.get_first())
                    history = ticker.history(period="3mo", interval="1d")[['Close', 'Open', 'High', 'Volume', 'Low']]
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

            self.latest_df = self.algo(history)
            print(self.latest_df)
            time.sleep(3) # Should be a wait function for a barrier
            

    # Cette fonction pourrait être un peu plus spécifique en ce qui concerne l'information "fetché"
    def fetch_data(self, symbol: str):
        n_ticker = yf.Ticker(symbol)

        # Option de sauvegarder dans un .csv
        '''
        ticker_history.to_csv(path/to/csv)
        '''
        self.num_API_calls += 1

        return n_ticker
    
    def start(self):
        self._thread.start()

    def stop(self):
        self.flag.set()

    def is_alive(self):
        return self._thread.is_alive()

    def join(self):
        self._thread.join()

    def name(self):
        return self.name

    def symbols(self):
        return self.symbols

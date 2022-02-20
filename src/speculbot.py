import yfinance as yf
import requests
from threading import Event, Thread

from yfinance.ticker import Ticker

class BotTicker:

    def __init__(self, symbol: str):
        self._name = symbol
        self._states = [-1]
        self._result = -1

    def add_state(self, state: int):
        self._result = state
        self._states.append(state)

    @property
    def states(self):
        return self._states

    @property
    def name(self):
        return self._name
    
    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result: int):
        self._result = result

class SpeculBot:

    def __init__(self, algo, symbols:str, name="SpeculBot", stop_loss=[]):
        self.flag = Event()

        # Set stop loss to assigned values
        if stop_loss == []:
            self.stop_loss_ref = [-0.03 for _ in symbols.split(' ')]
        else:
            self.stop_loss_ref = stop_loss

        # API vars
        self.num_API_calls = 0
        self.symbols = symbols
        self.tickers = [BotTicker(s) for s in symbols.upper().split(' ')]

        # Class properties
        self.name = name

        # Algorithm to run
        self.algo = algo

        # Donnée devant être transmise au contrôleur StockBoy
        self.latest_df = None
        self._thread = Thread(target=self.run)

    def run(self):
        while not self.flag.is_set():
            continue #TBD
    
    def get_results(self):
        history = None
        try:
            history = self.fetch_data(self.symbols)

        except Exception as ex:
            if type(ex) is ValueError:
                print("Yahoo Finance Backed Error, Attempting to Fix")
            elif type(ex) is requests.exceptions.SSLError:
                print("Yahoo Finance Backed Error, Attempting to Fix SSL")
            else:
                print("{err}".format(err=ex))

        self.algo(self.tickers, history, stop_loss=self.stop_loss_ref)

        return self.tickers

    def add_ticker(self, symbol: str):
        self.tickers.append(BotTicker(symbol))
        self.symbols += f" {symbol}"

    # Cette fonction pourrait être un peu plus spécifique en ce qui concerne l'information "fetché"
    def fetch_data(self, symbols):
        ticker_data = yf.download(symbols, period="1y", interval="1d")

        self.num_API_calls += 1
        return ticker_data
    
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

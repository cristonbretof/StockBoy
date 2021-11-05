import yfinance as yf
import requests
from collections import deque
from threading import Event, Thread

from yfinance.ticker import Ticker

SELL = "SELL"
BUY = "BUY"
TBD = "TBD"

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

    def __init__(self, algo, symbol, name="SpeculBot", stop_loss=-0.03):
        self.flag = Event()

        # API vars
        self.num_API_calls = 0
        self.ticker = symbol

        # Class properties
        self.name = name

        # Algorithm to run
        self.algo = algo

        # Runtime BUY/SELL signals emitted
        self.buysell_states = [-1]

        # Donnée devant être transmise au contrôleur StockBoy
        self.latest_df = None
        self._thread = Thread(target=self.run)

        self.stop_loss_ref = stop_loss

    def run(self):
        while not self.flag.is_set():
            continue #TBD
    
    def get_results(self):
        history = None
        try:
            ticker = self.fetch_data(self.ticker)
            # XXX DO NOT TOUCH THE "1y" XXX
            history = ticker.history(period="1y", interval="1d")[['Close', 'Open', 'High', 'Volume', 'Low']]

        except Exception as ex:
            if type(ex) is ValueError:
                print("Yahoo Finance Backed Error, Attempting to Fix")
            elif type(ex) is requests.exceptions.SSLError:
                print("Yahoo Finance Backed Error, Attempting to Fix SSL")
            else:
                print("{err}".format(err=ex))

        results = self.algo(history, self.buysell_states[-1], stop_loss=self.stop_loss_ref)

        if results == 1:
            self.buysell_states.append(results)
            return (self.ticker, BUY)
        elif results == 0:
            self.buysell_states.append(results)
            return (self.ticker, SELL)
        else:
            return results

    # Cette fonction pourrait être un peu plus spécifique en ce qui concerne l'information "fetché"
    def fetch_data(self, symbols):
        n_ticker = yf.Ticker(symbols)

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

import yfinance as yf
import argparse

from src.speculbot import BotTicker
from src.algos import algos

def test_algo(algo, tickers: list, history, *params):
    return algo(tickers, history, params or [])

symbols = "fb amzn aapl msft googl pypl adbe nvda tsla nflx ma cni shop uco jnj pg v hd cvx"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("algo",
                    help="Algorithm to test")
    args = parser.parse_args()

    try:
        # Get algo function from existing algorithms
        algo = getattr(algos, args.algo)
        
        history = yf.download(symbols, period="1y", interval="1d")

        tickers = [BotTicker(s) for s in symbols.upper().split(' ')]
        data = test_algo(algo, tickers, history)

        print(data)

    except AttributeError:
        print(f"First argument <algo> must contain a valid algorithm to run")



import time
import threading

from botcontroller import BotController
from src.algos.algos import *


def main():

    bc = BotController()
    bc.add_speculbot(algo=macd, symbols=["TQQQ", "GME", "AAPL", "GOOG"], name="TEST")
    bc.add_speculbot(algo=macd, symbols=["ETH", "BTC", "USD"], name="TOTO")
    bc.add_speculbot(algo=macd, symbols=["A", "AA", "AMC"], name="TATA")

    try:
        while len(threading.enumerate()) > 1:
            time.sleep(10)
            break

        bc.shutdown()

    except KeyboardInterrupt:
        print(" ---- END OF PROGRAM")
        quit()

if __name__ == "__main__":
    main()
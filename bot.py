import sys, time
from src.SpeculBot import SpeculBot
from threading import Thread


def main():
    spec = SpeculBot(["GME"])

    t1 = Thread(target=spec.run)
    t1.start()

    try:

        while t1.is_alive:
            time.sleep(1)
            continue
    except KeyboardInterrupt:
        print(" ---- END OF PROGRAM")
        spec.stop()
        quit()

if __name__ == "__main__":
    main()
import time
from pandas.core.frame import DataFrame


def macd(tickers: list, history, stop_loss: list):
    prices = []
    print(f"LOGGING REPORT -> {time.ctime()}")
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    for ticker, sl in zip(tickers, stop_loss):
        for price in history['Close'][ticker.name]:
            prices.append(price)

        prices_df = DataFrame(prices)  # Make a dataframe from the prices list

        # Calculate exponential weighted moving averages:
        day12 = prices_df.ewm(span=12).mean()
        day26 = prices_df.ewm(span=26).mean()
        macd = day12 - day26

        signal = macd.ewm(span=9).mean()

        current_state = -1
        last_state = ticker.states[-1]

        # Information sur la deniere analyse, soit buy ou sell
        compar = macd.iloc[-1][0] - signal.iloc[-1][0]
        if compar > 0:
            current_state = 1
        elif compar <= 0:
            current_state = 0

        closing_yesterday = prices_df.iloc[-2][0]
        closing_today = prices_df.iloc[-1][0]

        print(f"Stock = {ticker.name}")
        print(f"Current State: {current_state}, Last State: {last_state}")
        print(f"MACD: {macd.iloc[-1][0]}, Signal: {signal.iloc[-1][0]}")

        if current_state == 1:
            ratio = (closing_today - closing_yesterday)/closing_yesterday
            if ratio < sl:
                print(f"Stop loss occured: ratio={ratio}  target_sl={sl}")

                ticker.add_state(0)

                # Pour empêcher plusieurs SELL signal en rafale
                if ticker.states[-2] == ticker.states[-1]:
                    ticker.result = -1
                continue

        if current_state == 1 and last_state <= 0:
            ticker.add_state(1)
            continue
        elif current_state == 0 and last_state == 1:
            ticker.add_state(0)
            continue
        elif current_state == 0 and last_state == -1:
            ticker.add_state(0)
            continue
        elif current_state == last_state:
            ticker.result = -1
            continue

def momentum(tickers: list, history, *params):
    tabarnakesti = []
    print(f"LOGGING REPORT -> {time.ctime()}")
    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    for ticker in tickers:
        prices = []
        for price in history['Close'][ticker.name]:
            prices.append(price)

        prices_df = DataFrame(prices)
        
        closing_16    = prices_df.iloc[-17][0]
        closing_today = prices_df.iloc[-1][0]

        fuck = (closing_today/closing_16)-1
        tabarnakesti.append((fuck, ticker.name))

    # Sort all cumulative return
    sorted_tabarnakesti = sorted(tabarnakesti, reverse=True)

    # Extract top 2
    first_ticker = sorted_tabarnakesti[0]
    second_ticker = sorted_tabarnakesti[1]

    return (first_ticker[1], second_ticker[1])
import pandas
from pandas.core.frame import DataFrame


def macd(history, last_state, stop_loss):
    prices = []

    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    for price in history['Close']:
        prices.append(price)

    prices_df = DataFrame(prices)  # Make a dataframe from the prices list

    # Calculate exponential weighted moving averages:
    day12 = prices_df.ewm(span=12).mean()
    day26 = prices_df.ewm(span=26).mean()
    macd = day12 - day26

    signal = macd.ewm(span=9).mean()

    current_state = -1

    # Information sur la deniere analyse, soit buy ou sell
    compar = macd.iloc[-1][0] - signal.iloc[-1][0]
    if compar > 0:
        current_state = 1
    elif compar <= 0:
        current_state = 0

    closing_yesterday = prices_df.iloc[-2][0]
    closing_today = prices_df.iloc[-1][0]

    if current_state == 1:
        ratio = (closing_yesterday - closing_today)/closing_yesterday
        if ratio < stop_loss:
            return 0

    if current_state == 1 and last_state <= 0:
        return 1
    elif current_state == 0 and last_state == 1:
        return 0
    elif current_state == 0 and last_state == -1:
        return 0
    elif current_state == last_state:
        return -1
import pandas
from pandas.core.frame import DataFrame


def macd(history, last_state):
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

    # Recompose data into results
    # history.insert(0, 'MACD', macd)
    # history.insert(0, 'Signal', signal)

    # print(history)

    # current_state = -1
    # # Information sur la deniere analyse, soit buy ou sell
    # compar = macd.iloc(-1) - signal.iloc(-1)
    # if compar > 0:
    #     current_state = 1
    # elif compar <= 0:
    #     current_state = 0

    # if current_state > last_state:
    #     return 1
    # elif current_state < last_state:
    #     return 0
    # else:
    return -1
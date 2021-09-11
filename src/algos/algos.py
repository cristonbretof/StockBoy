from pandas.core.frame import DataFrame

def macd(history):
    # This list holds the closing prices of a stock
    prices = []

    # Add the closing prices to the prices list and make sure we start at greater than 2 dollars to reduce outlier calculations.
    for price in history['Close']:
        if price > float(2.00):  # Check that the closing price for this day is greater than $2.00
            prices.append(price)
    
    prices_df = DataFrame(prices)  # Make a dataframe from the prices list

    # Calculate exponential weighted moving averages:
    day12 = prices_df.ewm(span=12, adjust=False).mean()
    day26 = prices_df.ewm(span=26, adjust=False).mean()
    macd = day12 - day26

    signal = macd.ewm(span=9, adjust=False).mean()

    condiv = macd - signal

    # Recompose data into results
    history.insert(0, 'MACD', macd)
    history.insert(0, 'Signal', signal)
    history.insert(0, 'ConvDiv', condiv)

    return history
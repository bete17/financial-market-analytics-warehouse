#imports


#functions
    
def calc_daily_returns(prices):
    """Calculates the daily returns of a price series in percentage terms.

    Args:
        prices (pd.Series): A series of prices.

    Returns:
        pd.Series: A series of daily returns.
    """
    
    return prices.pct_change()

def calc_dollar_volume(volume, prices):
    """Calculates the daily volume of a volume series in dollar amounts.

    Args:
        volume (pd.Series): A series of volumes.
        price (pd.Series): A series of prices.
    Returns:
        pd.Series: A series of daily volumes.
    """
    return volume * prices

def calc_moving_average(prices, window):
    """Calculates the moving average of a price series.

    Args:
        prices (pd.Series): A series of prices.
        window (int): The window size for the moving average.

    Returns:
        pd.Series: A series of moving averages.
    """
    return prices.rolling(window=window).mean()

def create_stock_performance(df):
    """Creates a performance summary for a stock.

    Args:
        df (pd.DataFrame): A DataFrame containing stock data.

    Returns:
        pd.DataFrame: A DataFrame containing the performance summary.
    """
    return df.agg({
        'close': ['first', 'last', 'max', 'min'],
        'volume': 'sum'
    })

def create_volume_summary(df):
    """Creates a volume summary for a stock.

    Args:
        df (pd.DataFrame): A DataFrame containing stock data.

    Returns:
        pd.DataFrame: A DataFrame containing the volume summary.
    """
    return df.agg({
        'volume': ['first', 'last', 'max', 'min', 'sum']
    })
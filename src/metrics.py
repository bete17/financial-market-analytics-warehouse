import pandas as pd


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


def create_gold_performance_summary(df):
    """Create one performance summary row per ticker for the gold layer."""
    price_column = "adj_close" if "adj_close" in df.columns else "close"
    sorted_df = df.sort_values(["ticker", "date"])

    summary = sorted_df.groupby("ticker").agg(
        start_date=("date", "first"),
        end_date=("date", "last"),
        start_price=(price_column, "first"),
        end_price=(price_column, "last"),
        average_daily_return=("daily_return", "mean"),
        volatility=("daily_return", "std"),
        average_volume=("volume", "mean"),
        average_dollar_volume=("dollar_volume", "mean"),
    ).reset_index()

    summary["total_return"] = summary["end_price"] / summary["start_price"] - 1
    return summary[
        [
            "ticker",
            "start_date",
            "end_date",
            "start_price",
            "end_price",
            "total_return",
            "average_daily_return",
            "volatility",
            "average_volume",
            "average_dollar_volume",
        ]
    ]


def create_gold_moving_averages(df, windows=(20, 50)):
    """Add moving average columns per ticker for the gold layer."""
    price_column = "adj_close" if "adj_close" in df.columns else "close"
    result = df.sort_values(["ticker", "date"]).copy()

    for window in windows:
        result[f"ma_{window}"] = result.groupby("ticker")[price_column].transform(
            lambda prices: calc_moving_average(prices, window)
        )

    columns = ["date", "ticker", price_column, "close", "volume"]
    columns.extend([f"ma_{window}" for window in windows])
    available_columns = [column for column in columns if column in result.columns]
    return result[available_columns]


def create_gold_volume_summary(df):
    """Create a volume summary row per ticker for the gold layer."""
    sorted_df = df.sort_values(["ticker", "date"])

    return sorted_df.groupby("ticker").agg(
        start_date=("date", "first"),
        end_date=("date", "last"),
        min_volume=("volume", "min"),
        max_volume=("volume", "max"),
        total_volume=("volume", "sum"),
        average_volume=("volume", "mean"),
        average_dollar_volume=("dollar_volume", "mean"),
    ).reset_index()
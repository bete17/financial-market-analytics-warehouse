"""
transformations.py

This module contains functions for cleaning and standardizing stock price data.
These functions support the Silver layer of the project.
"""

import pandas as pd

from metrics import calc_daily_returns, calc_dollar_volume

PRICE_COLUMNS = ["open", "high", "low", "close", "adj_close"]
ESSENTIAL_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def standardize_column_names(df):
    """
    Standardize column names into a consistent format.

    Example:
        "Date" -> "date"
        "Adj Close" -> "adj_close"

    Parameters:
        df (DataFrame): Raw stock price data.

    Returns:
        DataFrame: Data with standardized column names.
    """
    standardized = df.copy()
    standardized.columns = (
        standardized.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
    )
    return standardized


def convert_data_types(df):
    """
    Convert columns to appropriate data types.

    Expected conversions:
        date -> datetime/date
        open, high, low, close, adj_close -> numeric
        volume -> integer

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Stock price data with corrected data types.
    """
    converted = df.copy()

    if "date" in converted.columns:
        converted["date"] = pd.to_datetime(converted["date"], errors="coerce")

    for column in PRICE_COLUMNS:
        if column in converted.columns:
            converted[column] = pd.to_numeric(converted[column], errors="coerce")

    if "volume" in converted.columns:
        converted["volume"] = pd.to_numeric(converted["volume"], errors="coerce")
        converted["volume"] = converted["volume"].round().astype("Int64")

    return converted


def remove_duplicate_rows(df):
    """
    Remove duplicate rows from the stock price data.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Stock price data without duplicate rows.
    """
    duplicate_columns = ["ticker", "date"] if "ticker" in df.columns else ["date"]
    return df.drop_duplicates(subset=duplicate_columns, keep="last")


def handle_missing_values(df):
    """
    Handle missing values in the stock price data.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Stock price data after missing value handling.
    """
    cleaned = df.copy()

    if "adj_close" in cleaned.columns and "close" in cleaned.columns:
        cleaned["adj_close"] = cleaned["adj_close"].fillna(cleaned["close"])

    required_columns = [
        column for column in ESSENTIAL_COLUMNS + ["ticker"] if column in cleaned.columns
    ]
    return cleaned.dropna(subset=required_columns)


def sort_stock_data(df):
    """
    Sort stock data by ticker and date.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Sorted stock price data.
    """
    sort_columns = ["ticker", "date"] if "ticker" in df.columns else ["date"]
    return df.sort_values(sort_columns).reset_index(drop=True)


def select_silver_columns(df):
    """
    Select and order the columns needed for the Silver layer.

    Expected columns:
        date
        ticker
        open
        high
        low
        close
        adj_close
        volume
        source
        loaded_at

    Parameters:
        df (DataFrame): Cleaned stock price data.

    Returns:
        DataFrame: Stock price data with selected Silver columns.
    """
    silver = df.copy()

    if "source_file" in silver.columns and "source" not in silver.columns:
        silver = silver.rename(columns={"source_file": "source"})

    silver_columns = [
        "date",
        "ticker",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
        "daily_return",
        "dollar_volume",
        "source",
        "loaded_at",
    ]
    available_columns = [column for column in silver_columns if column in silver.columns]
    return silver[available_columns]


def clean_stock_data(df):
    """
    Run all transformation steps for the Silver layer.

    Parameters:
        df (DataFrame): Bronze stock price data.

    Returns:
        DataFrame: Cleaned Silver stock price data.
    """
    cleaned = standardize_column_names(df)
    cleaned = convert_data_types(cleaned)
    cleaned = remove_duplicate_rows(cleaned)
    cleaned = handle_missing_values(cleaned)
    cleaned = sort_stock_data(cleaned)

    price_column = "adj_close" if "adj_close" in cleaned.columns else "close"
    if price_column in cleaned.columns:
        if "ticker" in cleaned.columns:
            cleaned["daily_return"] = cleaned.groupby("ticker")[price_column].transform(
                calc_daily_returns
            )
        else:
            cleaned["daily_return"] = calc_daily_returns(cleaned[price_column])

    if "volume" in cleaned.columns and "close" in cleaned.columns:
        cleaned["dollar_volume"] = calc_dollar_volume(cleaned["volume"], cleaned["close"])

    return select_silver_columns(cleaned)

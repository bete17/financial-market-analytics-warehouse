"""
transformations.py

This module contains functions for cleaning and standardizing stock price data.
These functions support the Silver layer of the project.
"""


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
    pass


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
    pass


def remove_duplicate_rows(df):
    """
    Remove duplicate rows from the stock price data.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Stock price data without duplicate rows.
    """
    pass


def handle_missing_values(df):
    """
    Handle missing values in the stock price data.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Stock price data after missing value handling.
    """
    pass


def sort_stock_data(df):
    """
    Sort stock data by ticker and date.

    Parameters:
        df (DataFrame): Stock price data.

    Returns:
        DataFrame: Sorted stock price data.
    """
    pass


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
    pass


def clean_stock_data(df):
    """
    Run all transformation steps for the Silver layer.

    Parameters:
        df (DataFrame): Bronze stock price data.

    Returns:
        DataFrame: Cleaned Silver stock price data.
    """
    pass
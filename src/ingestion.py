
"""
ingestion.py

This module contains functions for loading raw stock price data.
These functions support the Bronze layer of the project.
"""
import pandas as pd
import yfinance as yf
from pathlib import Path

YFINANCE_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]

def download_stock_csv(ticker, output_path, start_date=None, end_date=None, period="1y"):
    """
    Download historical stock prices from Yahoo Finance and save as CSV.

    Parameters:
        ticker (str): Stock ticker symbol (e.g. "AAPL").
        output_path (str): Destination path for the CSV file.
        start_date (str, optional): Start date in YYYY-MM-DD format.
        end_date (str, optional): End date in YYYY-MM-DD format.
        period (str): Lookback period when start/end are not provided (e.g. "1y", "6mo").

    Returns:
        DataFrame: Downloaded stock price data.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    stock = yf.Ticker(ticker)
    if start_date and end_date:
        df = stock.history(start=start_date, end=end_date, auto_adjust=False)
    else:
        df = stock.history(period=period, auto_adjust=False)

    if df.empty:
        raise ValueError(f"No data returned for ticker: {ticker}")

    df = df.reset_index()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)

    df = df[YFINANCE_COLUMNS]
    df.to_csv(path, index=False)
    return df


def load_stock_csv(file_path):
    """
    Load a single stock CSV file.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Raw stock price data.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(path)

    return df
    


def load_multiple_stock_csvs(folder_path):
    """
    Load multiple stock CSV files from a folder.

    Parameters:
        folder_path (str): Path to the folder containing CSV files.

    Returns:
        DataFrame: Combined raw stock price data.
    """
    final_df = pd.DataFrame()
    for file in Path(folder_path).glob("*.csv"):
        df = load_stock_csv(file)
        final_df = pd.concat([final_df, df], ignore_index=True)
    return final_df


def add_ingestion_metadata(df, file_path):
    """
    Add ingestion metadata to the raw stock data.

    Parameters:
        df (DataFrame): Raw stock price data.
        file_path (str): Path to the source file.

    Returns:
        DataFrame: Stock data with source_file and loaded_at columns.
    """
    path = Path(file_path)
    new_df = df.copy()
    new_df['source_file'] = path.name
    new_df['ticker'] = path.stem
    new_df['loaded_at'] = pd.Timestamp.now(tz='UTC')
    return new_df


def save_bronze_data(df, output_path):
    """
    Save raw stock data to the Bronze layer.

    Parameters:
        df (DataFrame): Raw stock price data.
        output_path (str): Destination path for saved Bronze data.

    Returns:
        None
    """
    path = Path(output_path)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
    except OSError as e:
        raise OSError(f"Failed to save bronze data to {output_path}: {e}") from e
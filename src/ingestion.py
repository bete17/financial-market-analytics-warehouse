
"""
ingestion.py

This module contains functions for loading raw stock price data.
These functions support the Bronze layer of the project.
"""
import pandas as pd
from pathlib import Path

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
    df.to_csv(output_path, index=False)
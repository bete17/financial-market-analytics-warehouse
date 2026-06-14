
"""
ingestion.py

This module contains functions for loading raw stock price data.
These functions support the Bronze layer of the project.
"""
import pandas as pd
import numpy as np
import yfinance as yf


def load_stock_csv(file_path):
    """
    Load a single stock CSV file.

    Parameters:
        file_path (str): Path to the CSV file.

    Returns:
        DataFrame: Raw stock price data.
    """
    if file_path.exists():
        df = pd.read_csv(file_path)
    else:
        df = np.null
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
    for file in folder_path.glob("*.csv"):
        df = load_stock_csv(file)
        final_df = pd.concat([final_df, df], ignore_index=True)
    return final_df


def add_ingestion_metadata(df, source_file):
    """
    Add ingestion metadata to the raw stock data.

    Parameters:
        df (DataFrame): Raw stock price data.
        source_file (str): Name of the source file.

    Returns:
        DataFrame: Stock data with source_file and loaded_at columns.
    """
    new_df = df.copy()
    new_df['source_file'] = source_file
    new_df['ticker'] = source_file.split('.')[0]
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
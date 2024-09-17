import yfinance as yf
import pandas as pd


def get_stock_data(ticker, api_key, start_date='2020-01-01', end_date='2024-01-01'):
    """Fetch stock data from Yahoo Finance."""
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# TODO: Add support for multiple stock tickers
# - Fetch historical data for multiple stock symbols and test predictions.

# TODO: Add real-time data handling
# - Implement functions to fetch real-time stock prices for live predictions.

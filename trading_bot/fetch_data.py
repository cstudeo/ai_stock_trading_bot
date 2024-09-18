import yfinance as yf
import pandas as pd


def get_stock_data(ticker, api_key=None, start_date='2020-01-01', end_date='2024-01-01', is_backtest=False):
    """Fetch stock data from Yahoo Finance."""
    if is_backtest:
        # Use provided start and end dates for backtesting
        print(f"Fetching historical data for backtesting: {ticker} from {start_date} to {end_date}")
        stock_data = yf.download(ticker, start=start_date, end=end_date)
    else:
        # Fetch real-time data (for live trading) using yfinance, which defaults to latest available data
        print(f"Fetching live market data for: {ticker}")
        stock_data = yf.download(ticker, period='1d', interval='1m')  # Fetch live minute data for today

    return stock_data

# TODO: Add support for multiple stock tickers
# - Fetch historical data for multiple stock symbols and test predictions.

# TODO: Add real-time data handling
# - Implement functions to fetch real-time stock prices for live predictions.

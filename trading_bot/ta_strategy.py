import pandas as pd
import numpy as np

class TechnicalAnalysisStrategy:
    def __init__(self):
        pass

    def calculate_indicators(self, data):
        """Calculate all technical indicators."""
        data = self.calculate_rsi(data)
        data = self.calculate_macd(data)
        data = self.calculate_bollinger_bands(data)
        # Example: Calculate Simple Moving Average (SMA)
        data['SMA'] = data['Close'].rolling(window=20).mean()
        return data

    def evaluate(self, data):
        """Evaluate trading signals based on technical indicators."""
        data = self.calculate_indicators(data)
        latest_data = data.iloc[-1]
        if latest_data['Close'] > latest_data['SMA']:
            return 'BUY'
        elif latest_data['Close'] < latest_data['SMA']:
            return 'SELL'
        else:
            return 'HOLD'

    def calculate_rsi(self, data, period=14):
        """Calculate Relative Strength Index (RSI)."""
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data

    def calculate_macd(self, data, short_window=12, long_window=26, signal_window=9):
        """Calculate Moving Average Convergence Divergence (MACD)."""
        data['ema_short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
        data['ema_long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
        data['MACD'] = data['ema_short'] - data['ema_long']
        data['MACD_Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
        data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
        return data

    def calculate_bollinger_bands(self, data, window=20, num_std_dev=2):
        """Calculate Bollinger Bands."""
        data['rolling_mean'] = data['Close'].rolling(window=window).mean()
        data['rolling_std'] = data['Close'].rolling(window=window).std()
        data['Bollinger_Upper'] = data['rolling_mean'] + (data['rolling_std'] * num_std_dev)
        data['Bollinger_Lower'] = data['rolling_mean'] - (data['rolling_std'] * num_std_dev)
        return data

    def apply_strategies(self, data):
        """Apply all strategies (RSI, MACD, Bollinger Bands)."""
        data = self.calculate_indicators(data)
        return data

    # TODO: Add real-time data handling
    # - Implement functions to fetch real-time stock prices for live predictions.

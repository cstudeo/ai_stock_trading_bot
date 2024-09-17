import numpy as np
import pandas as pd

# Functions for stock indicators
# Note: Functions assume data index is 'Date' (DatetimeIndex)

# Simple Moving Average (SMA)
def SMA(data, period = 30, column='Close'):
    return data[column].rolling(window=period).mean()

# Exponential Moving Average (EMA)
def EMA(data, period = 20, column='Close'):
    return data[column].ewm(span=period,adjust = False).mean()


# Moving Average Convergence/Divergence (MACD)
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    #Calculate the Short Term Exponential Moving Average
    ShortEMA = EMA(data, period_short, column=column)
    #Calculate the Long Term Exponential Moving Average
    LongEMA = EMA(data, period_long, column=column)
    #Calculate MACD
    data['MACD'] = ShortEMA - LongEMA
    #Calculate the signal line
    data['Signal_Line'] = EMA(data, period_signal, column='MACD')

    return data


# Relative Strength Index (RSI)
def RSI(data, period = 14, column='Close'):
    delta = data[column].diff(1)
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    data['up'] = up
    data['down'] = down 
    AVG_Gain = SMA(data, period, column = 'up')
    AVG_Loss = abs(SMA(data, period, column = 'down'))
    RS = AVG_Gain / AVG_Loss
    RSI = 100.0 - (100.0/(1.0 + RS))

    data['RSI'] = RSI

    return data

# Bollinger Bands
def BollingerBands(data, period=20, column='Close'):
    data['SMA'] = data[column].rolling(window=period).mean()
    data['stddev'] = data[column].rolling(window=period).std()
    data['Upper Band'] = data['SMA'] + (data['stddev'] * 2)
    data['Lower Band'] = data['SMA'] - (data['stddev'] * 2)
    return data

# Stochastic Oscillator
def StochasticOscillator(data, period=14, column='Close'):
    data['L14'] = data['Low'].rolling(window=period).min()
    data['H14'] = data['High'].rolling(window=period).max()
    data['%K'] = (data[column] - data['L14']) * 100 / (data['H14'] - data['L14'])
    data['%D'] = data['%K'].rolling(window=3).mean()
    return data

# Average True Range (ATR)
def ATR(data, period=14):
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))
    data['True Range'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)
    data['ATR'] = data['True Range'].rolling(window=period).mean()
    return data

# On-Balance Volume (OBV)
def OBV(data, column='Close'):
    data['Daily Return'] = data[column].diff()
    data['Direction'] = np.where(data['Daily Return'] > 0, 1, -1)
    data['OBV'] = (data['Volume'] * data['Direction']).cumsum()
    return data

# Weighted Moving Average (WMA)
def WMA(data, period=30, column='Close'):
    weights = np.arange(1, period+1)
    return data[column].rolling(window=period).apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

# Hull Moving Average (HMA)
def HMA(data, period=20, column='Close'):
    half_length = int(period / 2)
    sqrt_length = int(np.sqrt(period))
    WMA_half = WMA(data, half_length, column)
    WMA_full = WMA(data, period, column)
    diff = 2 * WMA_half - WMA_full
    return diff.rolling(window=sqrt_length).mean()

# Triangular Moving Average (TMA)
def TMA(data, period=20, column='Close'):
    return data[column].rolling(window=period).mean().rolling(window=period).mean()

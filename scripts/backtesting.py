import pandas as pd
from ta_strategy import apply_strategies

def backtest_strategy(data, strategy_func):
    data = strategy_func(data)

    # Example: Simple backtest logic
    data['signal'] = 0
    data['signal'][data['macd'] > data['macd_signal']] = 1  # Buy signal
    data['signal'][data['macd'] < data['macd_signal']] = -1 # Sell signal

    # Calculate returns
    data['returns'] = data['close'].pct_change()
    data['strategy_returns'] = data['returns'] * data['signal'].shift(1)
    data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod() - 1

    return data

def main():
    stock_symbol = 'AAPL'
    data = pd.read_csv(f"data/{stock_symbol}_historical_data.csv")
    results = backtest_strategy(data, apply_strategies)
    print(results[['date', 'cumulative_returns']])

if __name__ == "__main__":
    main()

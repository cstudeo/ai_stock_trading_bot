import pandas as pd
from trading_bot.lstm_model import LSTMModel
from trading_bot.ta_strategy import TechnicalAnalysisStrategy

class Backtest:
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.positions = 0
        self.trade_log = []  # Stores information about each trade
        self.ta_strategy = TechnicalAnalysisStrategy()
        self.lstm_model = LSTMModel()

    def execute_trade(self, signal, stock_price):
        if signal == 'BUY' and self.balance >= stock_price:
            # Buy one unit of stock
            self.positions += 1
            self.balance -= stock_price
            self.trade_log.append({'action': 'BUY', 'price': stock_price})
            print(f"Bought at ${stock_price}")
        elif signal == 'SELL' and self.positions > 0:
            # Sell one unit of stock
            self.positions -= 1
            self.balance += stock_price
            self.trade_log.append({'action': 'SELL', 'price': stock_price})
            print(f"Sold at ${stock_price}")

    def calculate_profit(self):
        # Total profit/loss by comparing initial balance with current balance
        return self.balance - self.initial_balance

    def run(self, data, model_type='technical_analysis'):
        """Run the backtest based on the specified model type."""
        print(f"Running backtest using {model_type} model...")

        for i in range(len(data)):
            stock_price = data.iloc[i]['Close']

            # If using LSTM model for predictions
            if model_type == 'lstm':
                # Ensure we have enough data for the LSTM model's input (e.g., at least 60 days)
                if i < 60:
                    continue  # Skip the first 60 days to have enough data

                prediction = self.lstm_model.predict(data.iloc[i-60:i+1])  # Use the past 60 days of data
                signal = 'BUY' if prediction > stock_price else 'SELL'  # A simple logic to buy/sell based on prediction

            # If using Technical Analysis strategy
            elif model_type == 'technical_analysis':
                signal = self.ta_strategy.evaluate(data.iloc[:i+1])

            # Execute the trade based on the signal
            self.execute_trade(signal, stock_price)


    def print_results(self, ticker):
        """Print the summary of the backtest results."""
        total_profit = self.calculate_profit()
        num_trades = len(self.trade_log)
        buy_trades = len([trade for trade in self.trade_log if trade['action'] == 'BUY'])
        sell_trades = len([trade for trade in self.trade_log if trade['action'] == 'SELL'])

        print(f"\nBacktest Summary for {ticker}:")
        print(f"Initial Balance: ${self.initial_balance}")
        print(f"Final Balance: ${self.balance}")
        print(f"Total Profit: ${total_profit}")
        print(f"Total Trades: {num_trades}")
        print(f"Buy Trades: {buy_trades}")
        print(f"Sell Trades: {sell_trades}")

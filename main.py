import time
from trading_bot.fetch_data import get_stock_data
from trading_bot.lstm_model import LSTMModel
from trading_bot.ta_strategy import TechnicalAnalysisStrategy
from trading_bot.trade_executor import execute_trade

# Configuration for stock tickers and strategies
STOCK_TICKERS = ['AAPL', 'TSLA', 'GOOGL']  # Tickers to track
STRATEGY_TYPE = 'short-term'  # Can be 'short-term' or 'long-term'
TRADING_FREQUENCY = 60  # In seconds (1-minute frequency)
API_KEY = ''  # For accessing stock data

# Main function
def run_trading_bot():
    print("Starting trading bot...")

    # Initialize the LSTM model
    lstm_model = LSTMModel()

    # Initialize the Technical Analysis strategy
    ta_strategy = TechnicalAnalysisStrategy()

    # Start the trading loop
    while True:
        for ticker in STOCK_TICKERS:
            print(f"\nFetching data for {ticker}...")

            # Fetch market data
            stock_data = get_stock_data(ticker, API_KEY)

            if STRATEGY_TYPE == 'short-term':
                # Run the LSTM model prediction
                prediction = lstm_model.predict(stock_data)
                print(f"Prediction for {ticker}: {prediction}")
            elif STRATEGY_TYPE == 'long-term':
                # Run Technical Analysis strategy
                signal = ta_strategy.evaluate(stock_data)
                print(f"Signal for {ticker}: {signal}")

            # Execute trade based on model/strategy signals
            execute_trade(ticker, prediction if STRATEGY_TYPE == 'short-term' else signal)

        # Sleep for the defined frequency before the next cycle
        time.sleep(TRADING_FREQUENCY)

if __name__ == "__main__":
    try:
        run_trading_bot()
    except KeyboardInterrupt:
        print("Trading bot stopped manually.")
    except Exception as e:
        print(f"An error occurred: {e}")

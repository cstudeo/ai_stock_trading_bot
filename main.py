import time
from trading_bot.fetch_data import get_stock_data
from trading_bot.lstm_model import LSTMModel
from trading_bot.ta_strategy import TechnicalAnalysisStrategy
from trading_bot.trade_executor import execute_trade
from trading_bot.backtest import Backtest  # New import for backtesting

# Configuration for stock tickers and strategies
STOCK_TICKERS = ['AAPL', 'TSLA', 'GOOGL']  # Tickers to track
STRATEGY_TYPE = 'short-term'  # Can be 'short-term' or 'long-term'
TRADING_FREQUENCY = 60  # In seconds (1-minute frequency)
API_KEY = ''  # For accessing stock data
MODE = 'live'  # Can be 'live' or 'backtest'

# Main function for live trading
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

            try:
                if STRATEGY_TYPE == 'short-term':
                    # Run the LSTM model prediction
                    prediction = lstm_model.predict(stock_data)
                    if prediction is not None:
                        print(f"Prediction for {ticker}: {prediction}")
                    else:
                        print(f"Prediction for {ticker} could not be generated.")
                elif STRATEGY_TYPE == 'long-term':
                    # Run Technical Analysis strategy
                    signal = ta_strategy.evaluate(stock_data)
                    if signal is not None:
                        print(f"Signal for {ticker}: {signal}")
                    else:
                        print(f"Signal for {ticker} could not be generated.")
                else:
                    print(f"Unknown strategy type: {STRATEGY_TYPE}")
                    continue

                # Execute trade based on model/strategy signals
                trade_signal = prediction if STRATEGY_TYPE == 'short-term' else signal
                if trade_signal is not None:
                    execute_trade(ticker, trade_signal)
                else:
                    print(f"No trade executed for {ticker} due to missing trade signal.")

            except Exception as e:
                print(f"An error occurred while processing {ticker}: {e}")

        # Sleep for the defined frequency before the next cycle
        time.sleep(TRADING_FREQUENCY)


# Main function for backtesting
def run_backtest():
    print("Starting backtesting...")

    # Initialize backtest
    backtest = Backtest()

    # Run backtest on each ticker
    for ticker in STOCK_TICKERS:
        print(f"\nBacktesting for {ticker}...")

        # Fetch historical data for backtesting
        stock_data = get_stock_data(ticker, API_KEY, start_date='2020-01-01', end_date='2024-01-01', is_backtest=True)

        try:
            # Run the backtest based on the selected strategy
            if STRATEGY_TYPE == 'short-term':
                backtest.run(stock_data, model_type='lstm')
            elif STRATEGY_TYPE == 'long-term':
                backtest.run(stock_data, model_type='technical_analysis')
            else:
                print(f"Unknown strategy type: {STRATEGY_TYPE}")
                continue

            # Print backtest results
            backtest.print_results(ticker)

        except Exception as e:
            print(f"An error occurred during backtesting for {ticker}: {e}")


if __name__ == "__main__":
    try:
        if MODE == 'live':
            run_trading_bot()
        elif MODE == 'backtest':
            run_backtest()
        else:
            print(f"Invalid mode: {MODE}")
    except KeyboardInterrupt:
        print("Trading bot stopped manually.")
    except Exception as e:
        print(f"An error occurred: {e}")

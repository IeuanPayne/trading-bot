import yfinance as yf
import pandas as pd
import numpy as np

class TradingBot:
    def __init__(self, symbol, short_window=40, long_window=100):
        self.symbol = symbol
        self.short_window = short_window
        self.long_window = long_window
        self.signals = pd.DataFrame()
        self.position = 0

    def fetch_data(self):
        print(f"Fetching data for {self.symbol}...")
        self.data = yf.download(self.symbol, start="2023-01-01", end="2024-01-01")
        print("Data fetched successfully.")

    def generate_signals(self):
        print("Generating signals...")
        self.signals['price'] = self.data['Adj Close']
        self.signals['short_mavg'] = self.data['Adj Close'].rolling(window=self.short_window, min_periods=1).mean()
        self.signals['long_mavg'] = self.data['Adj Close'].rolling(window=self.long_window, min_periods=1).mean()
        self.signals['signal'] = 0
        self.signals['signal'][self.short_window:] = np.where(
            self.signals['short_mavg'][self.short_window:] > self.signals['long_mavg'][self.short_window:], 1, 0)
        self.signals['positions'] = self.signals['signal'].diff()
        print("Signals generated successfully.")

    def simulate_trading(self):
        print("Simulating trading...")
        for index, row in self.signals.iterrows():
            if row['positions'] == 1:
                print(f"Buy signal on {index}: Price = {row['price']}")
                self.position = 1
            elif row['positions'] == -1:
                print(f"Sell signal on {index}: Price = {row['price']}")
                self.position = 0
        print("Trading simulation completed.")

    def run(self):
        self.fetch_data()
        self.generate_signals()
        self.simulate_trading()

if __name__ == "__main__":
    bot = TradingBot('AAPL', short_window=40, long_window=100)
    bot.run()

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class TradingStrategy:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.signals = pd.DataFrame()
        
    def fetch_data(self):
        """Fetch historical data from Yahoo Finance"""
        try:
            self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
            print(f"Data fetched successfully for {self.symbol}")
            return True
        except Exception as e:
            print(f"Error fetching data: {e}")
            return False
    
    def calculate_moving_averages(self, short_window=20, long_window=50):
        """Calculate moving averages and generate trading signals"""
        if self.data is None:
            print("No data available. Please fetch data first.")
            return
        
        # Calculate moving averages
        self.data['SMA_Short'] = self.data['Close'].rolling(window=short_window).mean()
        self.data['SMA_Long'] = self.data['Close'].rolling(window=long_window).mean()
        
        # Generate signals
        self.signals = pd.DataFrame(index=self.data.index)
        self.signals['Signal'] = 0
        
        # Create signals: 1 for buy, -1 for sell
        self.signals['Signal'][short_window:] = np.where(
            self.data['SMA_Short'][short_window:] > self.data['SMA_Long'][short_window:], 1, -1
        )
        
        # Calculate daily returns
        self.signals['Daily_Return'] = self.data['Close'].pct_change()
        
        # Calculate strategy returns
        self.signals['Strategy_Return'] = self.signals['Signal'].shift(1) * self.signals['Daily_Return']
        
    def plot_strategy(self):
        """Plot the trading strategy results"""
        if self.data is None or self.signals.empty:
            print("No data or signals available. Please run the strategy first.")
            return
        
        # Create a figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot prices and moving averages
        ax1.plot(self.data.index, self.data['Close'], label='Price')
        ax1.plot(self.data.index, self.data['SMA_Short'], label='Short MA')
        ax1.plot(self.data.index, self.data['SMA_Long'], label='Long MA')
        
        # Plot buy/sell signals
        buy_signals = self.signals[self.signals['Signal'] == 1]
        sell_signals = self.signals[self.signals['Signal'] == -1]
        
        ax1.plot(buy_signals.index, self.data.loc[buy_signals.index, 'Close'], '^', 
                markersize=10, color='g', label='Buy Signal')
        ax1.plot(sell_signals.index, self.data.loc[sell_signals.index, 'Close'], 'v', 
                markersize=10, color='r', label='Sell Signal')
        
        ax1.set_title(f'Moving Average Strategy: {self.symbol}')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.legend()
        
        # Plot cumulative returns
        cumulative_returns = (1 + self.signals['Strategy_Return']).cumprod()
        ax2.plot(cumulative_returns.index, cumulative_returns, label='Strategy Returns')
        ax2.plot(cumulative_returns.index, (1 + self.signals['Daily_Return']).cumprod(), 
                label='Buy and Hold Returns')
        
        ax2.set_title('Cumulative Returns')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Cumulative Returns')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Set up the strategy
    symbol = "AAPL"  # Apple stock
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # Last year of data
    
    # Create and run the strategy
    strategy = TradingStrategy(symbol, start_date, end_date)
    if strategy.fetch_data():
        strategy.calculate_moving_averages(short_window=20, long_window=50)
        strategy.plot_strategy()

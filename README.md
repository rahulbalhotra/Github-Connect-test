# Algorithmic Trading Learning Project

This project is a simple implementation of an algorithmic trading strategy using Python. It demonstrates basic concepts of algorithmic trading including:

- Data fetching from Yahoo Finance
- Technical analysis using Moving Averages
- Signal generation
- Strategy backtesting
- Performance visualization

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Run the example strategy:
```bash
python algorithmic_trading.py
```

## Features

1. **Data Fetching**: Uses `yfinance` to fetch historical stock data
2. **Technical Analysis**: Implements Moving Average Crossover strategy
3. **Visualization**: Shows price movements, signals, and strategy performance
4. **Performance Tracking**: Calculates and displays cumulative returns

## Usage

The main script includes an example using Apple (AAPL) stock with:
- 20-day short-term moving average
- 50-day long-term moving average
- 1 year of historical data

To modify the strategy:
1. Change the stock symbol (e.g., "MSFT" for Microsoft)
2. Adjust the moving average windows
3. Modify the date range

## Learning Path

1. Start by understanding the Moving Average Crossover strategy
2. Experiment with different:
   - Time periods
   - Moving average windows
   - Stocks/assets
3. Add more technical indicators
4. Implement risk management
5. Add position sizing
6. Explore other strategies

## Next Steps

- Add more technical indicators (RSI, MACD, etc.)
- Implement risk management rules
- Add portfolio management
- Include transaction costs
- Add more sophisticated entry/exit rules

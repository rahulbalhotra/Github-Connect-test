from flask import Flask, render_template, jsonify, request
from algorithmic_trading import TradingStrategy
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    symbol = data.get('symbol', 'AAPL')
    days = int(data.get('days', 365))
    short_window = int(data.get('shortWindow', 20))
    long_window = int(data.get('longWindow', 50))
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    strategy = TradingStrategy(symbol, start_date, end_date)
    if not strategy.fetch_data():
        return jsonify({'error': 'Failed to fetch data'})
    
    strategy.calculate_moving_averages(short_window=short_window, long_window=long_window)
    
    # Prepare data for frontend
    dates = strategy.data.index.strftime('%Y-%m-%d').tolist()
    response_data = {
        'dates': dates,
        'price': strategy.data['Close'].tolist(),
        'shortMA': strategy.data['SMA_Short'].tolist(),
        'longMA': strategy.data['SMA_Long'].tolist(),
        'signals': strategy.signals['Signal'].tolist(),
        'returns': (1 + strategy.signals['Strategy_Return']).cumprod().tolist(),
        'buyHoldReturns': (1 + strategy.signals['Daily_Return']).cumprod().tolist()
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

import numpy as np
import random
import time
from flet.plotly_chart import PlotlyChart  # Import PlotlyChart from the correct submodule
import yfinance as yf
import plotly.graph_objs as go


# Function to get share info (price, percentage change, and volume)
def get_share_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='1d', interval='1m')

        if hist.empty:
            return {
                'price': None,
                'percentage_change': None,
                'volume': None
            }

        # Correct data access
        current_price = hist['Close'].iloc[-1]
        open_price = hist['Open'].iloc[0]
        volume = hist['Volume'].iloc[-1]
        percentage_change = ((current_price - open_price) / open_price) * 100

        return {
            'price': float(current_price),
            'percentage_change': float(percentage_change),
            'volume': int(volume)  # Convert volume to integer for clarity
        }
    except Exception as e:
        # Return None in case of error or invalid stock symbol
        print(f"Error fetching data for {ticker}: {e}")
        return {
            'price': None,
            'percentage_change': None,
            'volume': None
        }


# Function to generate graph and return it as a base64-encoded image
def get_share_graph(ticker, size):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='5d', interval='1h')  # 5 days of hourly data

    if hist.empty:
        return None

    # Create a Plotly line chart
    fig = go.Figure()

    # Add the trace for the 'Close' prices
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Closing Price'))

    # Set chart title and axis labels
    fig.update_layout(
        title=f'{ticker} - Last 5 Days Closing Prices',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        showlegend=True,
        template='plotly_dark',  # Optional: set a dark theme
    )

    # Format the X-axis ticks and adjust for readability
    fig.update_xaxes(tickformat="%Y-%m-%d", tickangle=-45, dtick="1d")  # Adjust format and rotation

    # Return Flet PlotlyChart with the generated figure
    return PlotlyChart(fig, original_size=size)

def predict_stock_trend(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Fetch 5 days of hourly data
        hist = stock.history(period='5d', interval='1h')

        if hist.empty:
            return "No data available for prediction"

        # Extract closing prices
        closing_prices = hist['Close'].values

        # Simple moving average over the last 3 time points (can adjust)
        short_moving_avg = np.mean(closing_prices[-3:])

        # Compare the last price with the short moving average
        last_price = closing_prices[-1]

        time.sleep(random.randint(2, 5))

        if last_price > short_moving_avg:
            return f"UP"
        else:
            return f"DOWN"
    except:
        return "Error while proccesing request"
import numpy as np
import random
import time
from flet.plotly_chart import PlotlyChart  # Import PlotlyChart from the correct submodule
import flet as ft
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


def get_share_graph(ticker, size, bgcol):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1mo', interval='1d')

    if hist.empty:
        return ft.Text(f"No data available for ${ticker}", color=ft.colors.RED)

    # Proceed with generating the graph if data is available
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Closing Price'))

    # Generate ticks for every 5 days
    tick_values = hist.index[::5]  # Get every 5th date from the index

    # Set custom background color using bgcol argument
    fig.update_layout(
        title=f'{ticker} - Last Month Closing Prices',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        showlegend=True,
        paper_bgcolor=bgcol,  # Set the outer (paper) background color
        template='plotly_dark',  # Optional: keep dark theme
        xaxis=dict(
            tickmode='array',  # Set tick mode to array
            tickvals=tick_values,  # Use the generated tick values
            ticktext=[date.strftime("%Y-%m-%d") for date in tick_values],  # Format tick labels
            tickangle=-45,  # Rotate labels for better visibility
        )
    )

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
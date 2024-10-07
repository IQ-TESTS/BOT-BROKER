import numpy as np
import random
import time
import plotly.graph_objs as go
import flet as ft
from flet.plotly_chart import PlotlyChart
import json
import yfinance as yf
import plotly.graph_objects as go


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

def update_graph(ticker, bgcol, text_color):
    # Load existing charts data from JSON file
    charts_dict = {}
    try:
        with open("assets/shares_graphs.json", "r") as f:
            charts_dict = json.load(f)  # Load existing data if the file exists
    except FileNotFoundError:
        pass  # If the file does not exist, we will create a new one later
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting with an empty dictionary.")

    # Fetch stock data from Yahoo Finance
    stock = yf.Ticker(ticker)
    hist = stock.history(period='1mo', interval='1d')

    # Check if data is available
    if hist.empty:
        charts_dict[ticker] = {"error": f"No data available for ${ticker}"}
    else:
        # Proceed with generating the candlestick graph if data is available
        fig = go.Figure()

        # Add candlestick trace using Open, High, Low, Close (OHLC) data
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            increasing_line_color='green',  # Bullish candles
            decreasing_line_color='red',  # Bearish candles
            name='Price'
        ))

        # Set custom background color and customize layout
        fig.update_layout(
            xaxis_title={
                'text': 'Date',
                'font': {'color': text_color, 'size': 14}  # Set x-axis title text color and size
            },
            yaxis_title={
                'text': 'Price (USD)',
                'font': {'color': text_color, 'size': 14}  # Set y-axis title text color and size
            },
            showlegend=False,  # Hide legend
            paper_bgcolor=bgcol,  # Set the outer background color
            plot_bgcolor=bgcol,  # Set plot (inner) background to white
            font=dict(color=text_color),  # Set default font color for all elements
            xaxis=dict(
                tickmode='array',
                tickvals=hist.index[::5],  # Generate ticks for every 5th date
                ticktext=[date.strftime("%Y-%m-%d") for date in hist.index[::5]],
                tickangle=-45,  # Rotate labels for better visibility
                rangeslider=dict(visible=False),  # Disable the range slider
                tickfont={'color': text_color}  # Set x-axis tick labels color
            ),
            yaxis=dict(
                showgrid=True,  # Show grid on the y-axis
                tickfont={'color': text_color}  # Set y-axis tick labels color
            ),
        )

        # Set grid lines to match the style in the image
        fig.update_xaxes(showgrid=True, gridcolor='lightgray')  # Gray grid lines on x-axis
        fig.update_yaxes(showgrid=True, gridcolor='lightgray')  # Gray grid lines on y-axis

        # Serialize the figure as a JSON string
        fig_json = fig.to_json()

        # Add or update the JSON for this chart in the dictionary under the ticker symbol
        charts_dict[ticker] = json.loads(fig_json)  # Convert the JSON string to a Python dict

    # Save the updated chart data as a JSON file
    with open("assets/shares_graphs.json", "w") as f:
        json.dump(charts_dict, f, indent=4)  # Save with indentation for readability

def get_share_graph(ticker, size, text_color, graph_height=None):
    # Load the JSON data from the specified file
    try:
        with open("assets/shares_graphs.json", "r") as f:
            charts_data = json.load(f)  # Load JSON data
    except FileNotFoundError:
        return ft.Text("No data", color=ft.colors.RED)
    except json.JSONDecodeError:
        return ft.Text("No data", color=ft.colors.RED)

    # Check if the ticker exists in the loaded JSON data
    if ticker not in charts_data:
        return ft.Text(f"No data available for ${ticker}", color=ft.colors.RED)

    # Retrieve the chart data for the specified ticker
    chart_data = charts_data[ticker]

    # Create a Plotly figure from the loaded JSON data
    fig = go.Figure()

    # Add traces to the figure based on the loaded JSON data
    for trace in chart_data['data']:
        if trace['type'] == 'candlestick':
            fig.add_trace(go.Candlestick(
                x=trace['x'],
                open=trace['open'],
                high=trace['high'],
                low=trace['low'],
                close=trace['close'],
                increasing_line_color='green',
                decreasing_line_color='red',
                name='Price'
            ))

    # Set layout attributes from JSON data
    fig.update_layout(chart_data['layout'])

    # Set font color for all text elements
    fig.update_layout(font=dict(color=text_color))

    # If a custom graph height is provided, update the layout height
    if graph_height:
        # Adjust the plot height but limit the area where the actual plot is rendered
        fig.update_layout(
            height=graph_height,
            yaxis=dict(
                domain=[0.1, 0.9],  # Set domain for the plot area to avoid text stretching
                automargin=True  # Automatically adjust margins to fit the text
            )
        )

    # Return the graph in Plotly chart format
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
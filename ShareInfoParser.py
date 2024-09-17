import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def get_share_info(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}'
    share_info = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()

    soup = BeautifulSoup(content, 'html.parser')

    # Extract current price
    price_tag = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
    if price_tag:
        try:
            price_text = price_tag.text.strip().replace(',', '')  # Remove commas for float conversion
            share_info['price'] = float(price_text)
        except ValueError:
            share_info['price'] = None  # Handle conversion error
    else:
        share_info['price'] = None

    # Extract percentage change
    percentage_change_tag = soup.find('fin-streamer', {'data-field': 'regularMarketChangePercent'})
    if percentage_change_tag:
        # Clean the percentage change value
        percentage_change_text = percentage_change_tag.text.strip()
        # Remove parentheses and percentage sign, then handle negative values
        percentage_change_text = percentage_change_text.replace('(', '').replace(')', '').replace('%', '')
        try:
            # Convert to float
            percentage_change = float(percentage_change_text)
            # If the text contains a minus sign or if it's within parentheses, it is negative
            if '−' in percentage_change_tag.text or '−' in percentage_change_text:
                percentage_change = -abs(percentage_change)
            share_info['percentage_change'] = percentage_change
        except ValueError:
            share_info['percentage_change'] = None  # Handle conversion error
    else:
        share_info['percentage_change'] = None

    return share_info

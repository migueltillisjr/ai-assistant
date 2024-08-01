import os
import requests
from ...config import *

ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY')

def get_weekly_stock_info(equity: str):
    access_token = ALPHAVANTAGE_KEY
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={equity}&apikey={access_token}'
    response = requests.get(url)
    if response.raise_for_status() == None:
        market_data = response.json()
        return market_data["Weekly Time Series"]


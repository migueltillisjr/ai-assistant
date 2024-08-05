import os
import requests
from ...config import *
from ...openai_custom import completions
# from ....error_handler import error_handler

INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY')

def get_weekly_stock_info(equity: str):
    access_token = ALPHAVANTAGE_KEY
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={equity}&apikey={access_token}'
    response = requests.get(url)
    if response.raise_for_status() == None:
        market_data = response.json()
        return market_data["Weekly Time Series"]


# @error_handler
def get_weekly_stock_insights(phrase: str, equity: str):
    stock_info = get_weekly_stock_info(equity)
    print(f"{phrase}: {stock_info}")
    return completions(phrase=f"{phrase}: {stock_info}")

#!/usr/bin/env python3.11
import openai
import os
from .actions import ActionFunctions
from .ui import UiFunctions
from .data import DataFunctions

openai.api_key = os.getenv('OPENAI_API_KEY')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY')

fqdn = "randomfqdn.infopioneer.dev"


def chatgpt_completions_example(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract and clarify the date and convert the date to the format YYYYMMDD from this phrase return only the converted date in relation to today, the current date {current_date()}. Also only return the numbers of the formatted date and nothing else all of the time. Provide no explanation: '{phrase}'"}
      ]
    )
    return response.choices[0].message.content.strip()


class Functions(ActionFunctions, UiFunctions, DataFunctions):
    def __init__(self):
        pass


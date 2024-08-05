import openai
#from openai import OpenAI
import os
from datetime import datetime,timezone
from functools import wraps
from .config import *

openai.api_key = os.getenv('OPENAI_API_KEY')


def completions(phrase: str):
    response = completion = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": phrase}
      ]
    )
    return response.choices[0].message.content.strip()
#!/usr/bin/env python3.11
import shutil
import openai
#from openai import OpenAI
import os
from datetime import datetime,timezone
import json
from flask import Flask, jsonify, request, render_template
from functools import wraps
import string
import random


openai.api_key = os.getenv('OPENAI_API_KEY')
fqdn = "randomfqdn.infopioneer.dev"


def current_date():
    # Get the current date and time in UTC
    current_gmt_datetime = datetime.now(timezone.utc)
    # Format the date as YYYY-MM-DD
    formatted_date_gmt = current_gmt_datetime.strftime('%Y-%m-%d')
    return formatted_date_gmt


def chatgpt_parse_date(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract and clarify the date and convirt the date to the format YYYYMMDD from this phrase return only the converted date in relation to today, the current date {current_date()}. Also only return the numbers of the formatted date and nothing else all of the time. Provide no explanation: '{phrase}'"}
      ]
    )

    return response.choices[0].message.content.strip()


class Functions:
    def get_random_digit():
        return random.randint(0,9)

    get_random_digit_JSON = {
        "name": "get_random_digit",
        "description": "Get a random digit",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_random_letters(count: int, case_sensitive: bool = False):
        return ''.join(random.choices(string.ascii_letters if case_sensitive else string.ascii_uppercase, k=count))

    get_random_letters_JSON = {
        "name": "get_random_letters",
        "description": "Get a string of random letters",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of letters to return"},
                "case_sensitive": {"type": "boolean", "description": "Whether to include lower-case letters.  Default only returns upper-case letters."}
            },
            "required": ["count"]
        }
    }


    def show_help():
        __help = [
                "Get a random letter or number",
                "Help",
                ]
        return __help

    show_help_JSON = {
        "name": "show_help",
        "description": "Show help",
        "parameters": {
        }
    }




if __name__ == '__main__':
    print(chatgpt_parse_date("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign today"))

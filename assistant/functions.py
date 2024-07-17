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
import emoji
import requests
from .reddit import get_reddit_instance, get_subreddit_info, get_user_info

openai.api_key = os.getenv('OPENAI_API_KEY')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
fqdn = "randomfqdn.infopioneer.dev"


def chatgpt_completions_example(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract and clarify the date and convert the date to the format YYYYMMDD from this phrase return only the converted date in relation to today, the current date {current_date()}. Also only return the numbers of the formatted date and nothing else all of the time. Provide no explanation: '{phrase}'"}
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

    def get_random_emoji(count: 3):
        emoji_list = ['😭', '😊', '😎', '🤩', '😁', '👍', '🔥', '🙏']
        return ''.join(random.choices(emoji_list, k=count))
    
    get_random_emoji_JSON = {
        "name": "get_random_emoji",
        "description": "Get a string of a random emoji",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of emojis to return"},
            },
            "required": ["count"]
        }
    }

    def get_instagram_user_info():
        access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        user_info_url = f"https://graph.instagram.com/me?fields=id,media_type,media_url,username,timestamp&access_token={access_token}"
        
        response = requests.get(user_info_url)
        if response.status_code == 200:
            user_info = response.json()
            return user_info 

    get_instagram_user_info_JSON = {
        "name": "get_instagram_user_info",
        "description": "Get user information of prompted instagram user",
        "parameters": {
            "type": "object",
            "properties": {},
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
    print(chatgpt_completions_example("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign today"))
    
    client_id = 'An62bVeTYec8Z19gyBOrtg'
    client_secret = 'VLwPcm9GUHHidlqCIbN7GJ7cqpGZ4w'
    user_agent = 'AI-assistant Integration/0.1 by CarbonMonoxide_0'
    
    reddit = get_reddit_instance(client_id, client_secret, user_agent)
    

    subreddit_name = "wallstreetbets"
    get_subreddit_info(reddit, subreddit_name)   
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
import requests
from ...integrations.alpha_advantage import get_weekly_stock_info as weekly_stock_info
from ...integrations.alpha_advantage import get_weekly_stock_insights
from ...integrations.reddit import Reddit
from ...openai_custom import completions

openai.api_key = os.getenv('OPENAI_API_KEY')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY')
fqdn = "randomfqdn.infopioneer.dev"


class ActionFunctions:
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
    
    def get_weekly_stock_info(equity: str):
        return weekly_stock_info(equity)
        
        
    get_weekly_stock_info_JSON = {
        "name":"get_weekly_stock_info",
        "description":"Gets weekly stock info requested from the user",
        "parameters": {
            "type": "object",
            "properties": {
                "equity": {"type": "string", "description":"Name of equity to track"}
            },
            "required":["equity"]
        }
    }

    def get_weekly_stock_knowledge(phrase: str, equity: str):
        return get_weekly_stock_insights(phrase=phrase, equity=equity) 
        
    get_weekly_stock_knowledge_JSON = {
        "name":"get_weekly_stock_knowledge",
        "description":"Gets weekly stock insights requested by the user. Such as give me a summary of a stock. Or insights of a stock.",
        "parameters": {
            "type": "object",
            "properties": {
                "phrase": {"type": "string", "description": "The phrase that initiated this request that represents what is being asked for."},
                "equity": {"type": "string", "description":"Name of equity to describe and get instights from."}
            },
            "required":["phrase","equity"]
        }
    }

    def get_subreddit_info(subreddit_name: str):
        return Reddit(subreddit_name).sub_reddit_info

    get_subreddit_info_JSON = {
        "name":"get_subreddit_info",
        "description":"Gets subreddit info for a particular subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit_name": {"type": "string", "description":"Name of subreddit"}
            },
            "required":["subreddit_name"]
        }
    }

    def catch_all(phrase):
        resp = completions(phrase=phrase)
        return resp

    catch_all_JSON = {
        "name": "catch_all",
        "description": "This function is to be used for general requests that don't match a particular defined function.",
        "parameters": {
            "type": "object",
            "properties": {
                "phrase": {"type": "string", "description": "The phrase that initiated this request that represents what is being asked for."},
            },
        "required":["phrase"],
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

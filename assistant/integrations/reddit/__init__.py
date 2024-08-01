#!/usr/bin/env python3.11

import os
import praw
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from collections import Counter 
import string 
import csv 
import requests 
import sqlite3

git_stopwords_list = requests.get("https://gist.githubusercontent.com/rg089/35e00abf8941d72d419224cfd5b5925d/raw/12d899b70156fd0041fa9778d657330b024b959c/stopwords.txt").content
git_stopwords = set(git_stopwords_list.decode().splitlines()) 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")
current_directory = os.path.dirname(os.path.abspath(__file__))

wallstreetbets_stopwords = ["stock" , "stocks", "market", "time", 
                            "year", "day", "days", "last", "week", 
                            "back", "price", "prices", "earnings", "options", 
                            "bought", "company","shares", "today", "trading", 
                            "2024", "post", "billion", "good", "position", 
                            "positions", "big", "view", "post", "moves", 
                            "update", "people", "months", "years", "yesterday", 
                            "tomorrow" "worth", "account", "business", "companies"
                           ]

# creates reddit instance using client id, client secret and user agent

def get_reddit_instance(client_id, client_secret, user_agent):
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=user_agent)

def get_user_info(reddit, username):
    try:
        user = reddit.redditor(username)
        user_info = {
            "name": user.name,
            "comment_karma": user.comment_karma,
            "link_karma": user.link_karma,
            "is_mod": user.is_mod,
            "is_gold": user.is_gold,
            "created_utc": user.created_utc
        }
        return user_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    


def get_subreddit_info(reddit, subreddit_name):
    try: 
    
        subreddit = reddit.subreddit(subreddit_name)

        hot_posts = subreddit.top(time_filter="week", limit=500)

        post_info = []

        for post in hot_posts:
            post_info.append({

                # metadata

                "Title": post.title,
                "Text": post.selftext,
                "Karma": post.score,
                "Author": str(post.author),
                "Time posted": post.created_utc

            })
        return post_info
    except Exception as e:
        print(f"An error occured: {e}")
        return None
      
def get_keywords(posts):
    words = []
    nltk_stopwords = set(stopwords.words('english'))
    for post in posts:
        text = post["Title"] + " " + post["Text"]
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokenized_words = word_tokenize(text)
        filtered_words = [word for word in tokenized_words if word.isalpha() and word not in nltk_stopwords and word not in git_stopwords and word not in wallstreetbets_stopwords] 

        words.extend(filtered_words)
    word_counts = Counter(words)
    popular_words = word_counts.most_common(20)
    return popular_words


def metadata_to_csv(posts, keywords, post_filename = f"{current_directory}/posts.csv", keywords_filename = f"{current_directory}/keywords.csv"):
    
    csv.register_dialect('custom', delimiter='`', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    # csv for post information
    with open(post_filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["Title", "Text", "Karma", "Author", "Time posted"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for post in posts:
            writer.writerow(post)

    # csv for important keywords and count
    with open(keywords_filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ["Keyword", "Count"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
        for word, amount in keywords:
            writer.writerow({"Keyword": word, "Count": amount})

def metadata_to_sql(posts, keywords, database=f"{current_directory}/metadata.db"):

    sql = sqlite3.connect(database)
    cursor = sql.cursor()
    try:
        with sql:
            cursor.execute("""CREATE TABLE IF NOT EXISTS posts(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                text TEXT,
                                karma INTEGER,
                                author TEXT,
                                time_posted REAL
                            )
                        
                        """)
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS keywords (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                keyword TEXT,
                                count INTEGER
                            )
                        """)
            for post in posts:
                cursor.execute("""
                            INSERT INTO posts (title, text, karma, author, time_posted) 
                            VALUES (?, ?, ?, ?, ?)
                            """, (post["Title"], post["Text"], post["Karma"], post["Author"], post["Time posted"]))
                
            for word, amount in keywords:
                cursor.execute('''
                INSERT INTO keywords (keyword, count) VALUES ( ?, ?)
                ''', (word, amount))
                
    finally:
        sql.close()       

    
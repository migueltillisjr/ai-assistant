#!/usr/bin/env python3.11

import os
import praw
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from collections import Counter 
import string 

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

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
    
def get_subreddit_info(reddit, subreddit):
    try: 
    
        subreddit = reddit.subreddit(subreddit_name)

        hot_posts = subreddit.top(time_filter="month", limit=500)

        post_info = []

        for post in hot_posts:
            post_info.append({
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
    stop_words = set(stopwords.words('english'))

    for post in posts:
        text = post["Title"] + " " + post["Text"]
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokenized_words = word_tokenize(text)
        filtered_words = [word for word in tokenized_words if word.isalnum() and word not in stop_words]

        words.extend(filtered_words)
    word_counts = Counter(words)
    popular_words = word_counts.most_common(10)
    return popular_words


if __name__ == "__main__":
    
    reddit = get_reddit_instance(CLIENT_ID, CLIENT_SECRET, USER_AGENT)
    
    username = 'CarbonMonoxide_0'  # Replace with the username you want to look up
   # user_info = get_user_info(reddit, username)

    subreddit_name = "wallstreetbets"
    posts = get_subreddit_info(reddit, subreddit_name)   



    
    if posts:
        keywords = get_keywords(posts)
        print("Popular keywords:")
        for word, amount in keywords:
            print(f"{word}: {amount}")
    else:
        print("Failed to retrieve user information.")
    

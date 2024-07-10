#!/usr/bin/env python3.11

import praw

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

if __name__ == "__main__":
    client_id = 'STRING_UNDER_APP_NAME'
    client_secret = 'SECRET_KEY'
    user_agent = 'APP_NAME/0.1 by USER_NAME'
    
    reddit = get_reddit_instance(client_id, client_secret, user_agent)
    
    username = 'example_username'  # Replace with the username you want to look up
    user_info = get_user_info(reddit, username)
    
    if user_info:
        print("User Information:")
        for key, value in user_info.items():
            print(f"{key}: {value}")
    else:
        print("Failed to retrieve user information.")


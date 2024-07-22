from . import (get_reddit_instance, get_subreddit_info, 
               get_keywords, CLIENT_ID, CLIENT_SECRET, USER_AGENT)

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
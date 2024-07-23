from .reddit import *

# print(chatgpt_completions_example("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign today"))

reddit = get_reddit_instance(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

subreddit_name = "wallstreetbets"
posts = get_subreddit_info(reddit, subreddit_name)   

if posts:
    keywords = get_keywords(posts)
    print("Popular keywords:")
    for word, amount in keywords:
        print(f"{word}: {amount}")
else:
    print("Failed to retrieve user information.")
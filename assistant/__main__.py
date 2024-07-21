from . import Assistant
AI = Assistant()
AI.send_message("return subreddit information from wallstreetbets")
print(AI.wait_on_run())
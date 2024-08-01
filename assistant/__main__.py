from . import Assistant

AI = Assistant()
AI.send_message("return subreddit information from wallstreetbets")
print(AI.wait_on_run())

AI = Assistant()
AI.send_message("Get weekly stock info from SPY")
print(AI.wait_on_run())
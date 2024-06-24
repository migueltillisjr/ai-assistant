#!/usr/bin/env python3.11
"""
A simple OpenAI Assistant with Functions.
The functions defined here in functions.py give the Assistant the ability to
generate random numbers and strings, which is something a base Assistant cannot do.

This module is designed to be used by gui.py, which provides a minimal terminal consisting of
- an input textbox for the user to type a message for the assistant
- an output textbox to display the assistant's response

User/assistant interactions are also written to LOGFILE (AssistantLog.md).
The complete OpenAI interactions are encoded in JSON and printed to STDOUT.

When creating the assistant, this module also stores the Assistant ID in .env, so as
to avoid recreating it in the future.  (A list of assistants that have been created
with your OpenAI account can be found at https://platform.openai.com/assistants)

REQUIREMENT: You will need an OPENAI_API_KEY, which should be stored in .env
See https://platform.openai.com/api-keys
"""
from datetime import datetime, timezone
import json
import os
import time
import openai
from functions import Functions

# Replace with your own OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

LOGFILE = 'AssistantLog.md'  # We'll store all interactions in this file

def current_date():
    # Get the current date and time in UTC
    current_gmt_datetime = datetime.now(timezone.utc)
    # Format the date as YYYY-MM-DD
    formatted_date_gmt = current_gmt_datetime.strftime('%Y-%m-%d')
    return formatted_date_gmt

class Assistant:
    def __init__(self):
        while openai.api_key is None:
            openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai
        self.create_AI_thread()

    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating assistant thread...')
        self.thread = {"id": "dummy_thread_id"}  # Simulate thread creation
        with open(LOGFILE, 'a+') as f:
            f.write(f'# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread["id"]}\n\n')

    def wait_on_run(self):
        """Waits for an OpenAI assistant run to finish and handles the response."""
        print('Waiting for assistant response...')
        response = self.run
        new_messages = response.choices
        response_text = ""
        with open(LOGFILE, 'a+') as f:
            f.write('\n**Assistant**:\n')
            for m in new_messages:
                msg = m.message["content"]
                f.write(msg)
                response_text += msg
            f.write('\n\n---\n')
        return response_text

    def send_message(self, message_text: str):
        """
        Send a message to the assistant.

        Parameters
        ----------
        message_text: str
            The message to send to the assistant.
        """
        print(f'\nSending message: {message_text}')
        self.run = self.client.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_text}
            ]
        )
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')

if __name__ == '__main__':
    AI = Assistant()
    AI.send_message("Give me a random number")
    print(AI.wait_on_run())


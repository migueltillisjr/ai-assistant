#!/usr/bin/env python3.11
"""
A simple OpenAI Assistant with Functions, created by David Bookstaber.
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

with open('chatgpt.directions.txt', 'r') as file:
    directions = file.read()

def show_json(obj):
    """Formats JSON for more readable output."""
    return json.dumps(json.loads(obj.model_dump_json()), indent=2)

class Assistant:
    def __init__(self, assistant_id=None):
        while openai.api_key is None:
            openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai
        self.ASSISTANT_ID = assistant_id
        self.build_assistant()
        self.create_AI_thread()


    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating assistant thread...')
        self.thread = self.client.beta.threads.create()
        print(show_json(self.thread))
        with open(LOGFILE, 'a+') as f:
            f.write(f'# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread.id}\n\n')


    def build_assistant(self):
        if not self.ASSISTANT_ID:  # Create the assistant
            print('Creating assistant...')
            assistant = self.client.beta.assistants.create(
                name="Ai Assistant",
                instructions=directions + "\n format all responses in json only",
                model="gpt-4",
                tools=[
                    {"type": "code_interpreter"},
                    {"type": "function", "function": Functions.get_random_digit_JSON},
                    {"type": "function", "function": Functions.get_random_letters_JSON},
                       ]
            )
            # Store the new assistant.id in .env
            self.ASSISTANT_ID = assistant.id
            print("ASSITANT ID:")
            print(self.ASSISTANT_ID)
        else:
            assistant = self.client.beta.assistants.update(
                assistant_id=self.ASSISTANT_ID,
                name="Ai Assistant",
                instructions=directions + "\n format responses in json and only the json portion of the response as a string.",
                model="gpt-4",
                tools=[
                    {"type": "code_interpreter"},
                    {"type": "function", "function": Functions.get_random_digit_JSON},
                    {"type": "function", "function": Functions.get_random_letters_JSON},
                       ]
            )
            print("ASSITANT ID:")
            print(self.ASSISTANT_ID)


    def wait_on_run(self, ):
        """Waits for an OpenAI assistant run to finish and handles the response."""
        print('Waiting for assistant response...')
        while self.run.status == "queued" or self.run.status == "in_progress":
            self.run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=self.run.id)
            time.sleep(1)
        if self.run.status == "requires_action":
            print(f'\nASSISTANT REQUESTS {len(self.run.required_action.submit_tool_outputs.tool_calls)} TOOLS:')
            tool_outputs = []
            for tool_call in self.run.required_action.submit_tool_outputs.tool_calls:
                tool_call_id = tool_call.id
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                print(f'\nAssistant requested {name}({arguments})')
                output = getattr(Functions, name)(**arguments)
                tool_outputs.append({"tool_call_id": tool_call_id, "output": json.dumps(output)})
                print(f'\n\tReturning {output}')
            self.run = self.client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread.id, run_id=self.run.id, tool_outputs=tool_outputs)
            return output
        else:
            # Get messages added after our last user message
            new_messages = self.client.threads.messages.list(thread_id=self.thread.id, order="asc", after=self.message.id)
            response = list()
            with open(LOGFILE, 'a+') as f:
                f.write('\n**Assistant**:\n')
                for m in new_messages:
                    msg = m.content[0].text.value
                    f.write(msg)
                    response.append(msg)
                f.write('\n\n---\n')
            # Callback to GUI with list of messages added after the user message we sent
            return str(response).replace('```json', '').replace('```', '').replace('\\n', '')


    def send_message(self, message_text: str):
        """
        Send a message to the assistant.

        Parameters
        ----------
        """
        self.message = self.client.beta.threads.messages.create(self.thread.id, role = "user", content = message_text)
        print('\nSending:\n' + show_json(self.message))
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.ASSISTANT_ID)
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')


if __name__ == '__main__':

    AI = Assistant("asst_KxXiqpptZ1pPBJray6lmoiFv")
    AI.send_message("return 3 random letters.")
    print(AI.wait_on_run())


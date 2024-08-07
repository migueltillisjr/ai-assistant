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
from .functions import Functions
from .integrations.reddit import Reddit
from assistant.config import *
import pandas as pd

# Replace with your own OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
GPT_DIRECTIONS = os.getenv('GPT_DIRECTIONS')
FINE_TUNING = os.getenv('FINE_TUNING')

openai.api_key = OPENAI_API_KEY

LOGFILE = 'assistant/files/AssistantLog.md'  # We'll store all interactions in this file

# opens the GPT's instructions
print("Opens GPT instructions")
with open(GPT_DIRECTIONS, 'r') as file:
    directions = file.read()

def show_json(obj):
    """Formats JSON for more readable output."""
    return json.dumps(json.loads(obj.model_dump_json()), indent=2)

tools = [
    {"type": "code_interpreter"},
    {"type": "file_search"},
    {"type": "function", "function": Functions.get_random_digit_JSON},
    {"type": "function", "function": Functions.get_random_letters_JSON},
    {"type": "function", "function": Functions.get_random_emoji_JSON},
    {"type": "function", "function": Functions.get_weekly_stock_info_JSON},
    {"type": "function", "function": Functions.get_subreddit_info_JSON},
    {"type": "function", "function": Functions.get_weekly_stock_knowledge_JSON},
]

class Assistant:
    def __init__(self, assistant_id=None):
        while openai.api_key is None:
            openai.api_key = os.getenv('OPENAI_API_KEY')
        self.client = openai
        self.ASSISTANT_ID = assistant_id
        self.build_assistant()
        self.create_AI_thread()
        self.files = list()
        self.vector_store_id = str()

    def csv_to_json(self, path):
        # Load the CSV file into a DataFrame
        csv_file_path = f'{path}'
        df = pd.read_csv(csv_file_path)

        # Convert the DataFrame to JSON
        json_result = df.to_json(orient='records', lines=True)

        # Save the JSON to a file
        json_file_path = f'{path}.json'
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_result)


    def get_absolute_paths(self, directory):
        # List to store the absolute paths
        absolute_paths = []

        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Create the full path
            full_path = os.path.join(directory, filename)
            
            # Check if it's a file (and not a directory)
            if os.path.isfile(full_path):
                absolute_paths.append(os.path.abspath(full_path))
        
        return absolute_paths
    
    def get_csv_file_paths(self, directory):
        # List to store the absolute paths of CSV files
        json_paths = []

        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Create the full path
            full_path = os.path.join(directory, filename)
            
            # Check if it's a file and if it has a .csv extension
            if os.path.isfile(full_path) and filename.endswith('.csv'):
                json_paths.append(os.path.abspath(full_path))
        
        return json_paths

    def get_json_file_paths(self, directory):
        # List to store the absolute paths of CSV files
        json_paths = []

        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Create the full path
            full_path = os.path.join(directory, filename)
            
            # Check if it's a file and if it has a .csv extension
            if os.path.isfile(full_path) and filename.endswith('.json'):
                json_paths.append(os.path.abspath(full_path))
        
        return json_paths
    
    def get_pdf_file_paths(self, directory):
        # List to store the absolute paths of CSV files
        json_paths = []

        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            # Create the full path
            full_path = os.path.join(directory, filename)
            
            # Check if it's a file and if it has a .csv extension
            if os.path.isfile(full_path) and filename.endswith('.pdf'):
                json_paths.append(os.path.abspath(full_path))
        
        return json_paths

    def delete_files(self, file_paths):
        for file_path in file_paths:
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")
            else:
                print(f"File not found: {file_path}")

    def create_vector_store(self):
        # Create a vector store caled "Financial Statements"
        vector_store = self.client.beta.vector_stores.create(name="ai-assistant")
        self.vector_store_id = vector_store.id
        # Ready the files for upload to OpenAI
        # file_paths = [f"{FINE_TUNING}"]
        for path in self.get_csv_file_paths(FINE_TUNING + '/original'):
            self.csv_to_json(path)

        json_file_paths = self.get_json_file_paths(FINE_TUNING + '/original')
        pdf_file_paths = self.get_pdf_file_paths(FINE_TUNING + '/original')
        file_streams = [open(path, "rb") for path in json_file_paths]
        file_streams = file_streams + [open(path, "rb") for path in pdf_file_paths]

        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
        )
        
        # You can print the status and the file counts of the batch to see the result of this operation.
        print(file_batch.status)
        print(file_batch.file_counts)
        self.delete_files(file_paths=json_file_paths)


    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating assistant thread...')
        self.thread = self.client.beta.threads.create()
        print(show_json(self.thread))

        with open(LOGFILE, 'a+') as f:
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread.id}\n\n')


    def build_assistant(self):
        self.create_vector_store()
        if not self.ASSISTANT_ID:  # Create the assistant
            print('Creating assistant...')
            # file_ids = self.upload_files(f'{FINE_TUNING}/original', f'{FINE_TUNING}/jsonl')
            assistant = self.client.beta.assistants.create(
                name="Ai Assistant",
                instructions=directions + "\n format all responses in json only",
                model="gpt-4o",
                tools=tools,
                tool_resources={"file_search": {"vector_store_ids": [self.vector_store_id]}}
            )
            # Store the new assistant.id in .env
            self.ASSISTANT_ID = assistant.id
            print("ASSISTANT ID:")
            print(self.ASSISTANT_ID)
        else:
            # file_ids = self.upload_files(f'{FINE_TUNING}/original', f'{FINE_TUNING}/jsonl')
            assistant = self.client.beta.assistants.update(
                assistant_id=self.ASSISTANT_ID,
                name="Ai Assistant",
                instructions=directions + "\n format responses in json and only the json portion of the response as a string.",
                model="gpt-4o",
                tools=tools,
                tool_resources={"file_search": {"vector_store_ids": [self.vector_store.id]}}
            )
            print("ASSISTANT ID:")
            print(self.ASSISTANT_ID)

    def wait_on_run(self):
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
            with open(LOGFILE, 'a+') as f:
                f.write('\n**Assistant**:\n')
                f.write(json.dumps(output))
                f.write('\n\n---\n')
            return output
        else:
            # Get messages added after our last user message
            new_messages = self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc", after=self.message.id)
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
            f.write('\n\n---\n')

    def send_message(self, message_text: str):
        """
        Send a message to the assistant.

        Parameters
        ----------
        """
        self.message = self.client.beta.threads.messages.create(self.thread.id, role="user", content=message_text)
        print('\nSending:\n' + show_json(self.message))
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.ASSISTANT_ID)
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')

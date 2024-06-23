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
from datetime import datetime,timezone
import json
import os
import time
from datetime import datetime
from openai import OpenAI
from functions import Functions
#dotenv.load_dotenv()
#OpenAI.api_key = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY="Use your own key!!!"
#OpenAI.api_key = ""
OpenAI.api_key=OPENAI_API_KEY
print(OpenAI.api_key)
ASSISTANT_ID = "asst_mh5wf4nJPDgpvBK8lAF8jCU6"

LOGFILE = 'AssistantLog.md'  # We'll store all interactions in this file
AI_RESPONSE = '-AIresponse-'  # GUI event key for Assistant responses
directions=str()


def current_date():
    # Get the current date and time in UTC
    current_gmt_datetime = datetime.now(timezone.utc)
    # Format the date as YYYY-MM-DD
    formatted_date_gmt = current_gmt_datetime.strftime('%Y-%m-%d')
    return formatted_date_gmt


def chatgpt_parse_date(phrase):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract and clarify the date and convirt the date to the format YYYYMMDD from this phrase return only the converted date in relation to today, the current date {current_date()}. Also only return the numbers of the formatted date and nothing else all of the time. Provide no explanation: '{phrase}'"}
      ]
    )

    return response.choices[0].message.content.strip()


def chatgpt_parse_response(message):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract the text here and convert to a purely text string and only the text string. Do not return as markup."}
          #{"role": "user", "content": f"Extract the text here and convert to a purely JSON string and only the json string. Do not return as markup."}
      ]
    )

    return response.choices[0].message.content.strip()


def chatgpt_parse_filename(message):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract the text here that represents a file name and convert to a purely JSON string and only the json string. Do not return as markup."}
      ]
    )

    return response.choices[0].message.content.strip()


with open('chatgpt.directions.txt', 'r') as file:
    directions = file.read()

def show_json(obj):
    """Formats JSON for more readable output."""
    return json.dumps(json.loads(obj.model_dump_json()), indent=2)

class Assistant:
    def __init__(self):
        while OpenAI.api_key is None:
            #input("Hey! Couldn't find OPENAI_API_KEY. Put it in .env then press any key to try again...")
            #dotenv.load_dotenv()
            OpenAI.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI()
        self.run = None
        self.message = None
        global ASSISTANT_ID
        if ASSISTANT_ID is None:  # Create the assistant
            assistant = self.client.beta.assistants.create(
                name="Random Assistant",
                instructions=directions + "\n format all responses in json only",
                model="gpt-4",
                tools=[
                    {"type": "code_interpreter"},
                    {"type": "function", "function": Functions.get_random_digit_JSON},
                    {"type": "function", "function": Functions.get_random_letters_JSON},
                    {"type": "function", "function": Functions.get_reports_JSON},
                    {"type": "function", "function": Functions.delete_campaigns_JSON},
                    {"type": "function", "function": Functions.list_campaigns_JSON},
                    {"type": "function", "function": Functions.schedule_email_campaign_JSON},
                    {"type": "function", "function": Functions.show_help_JSON},
                    {"type": "function", "function": Functions.update_contacts_JSON},
                    {"type": "function", "function": Functions.get_email_editor_JSON},
                    {"type": "function", "function": Functions.get_sample_email_text_JSON},
                    {"type": "function", "function": Functions.get_reports_JSON},
                    {"type": "function", "function": Functions.get_archived_reports_JSON},
                    {"type": "function", "function": Functions.get_archived_contact_lists_JSON},
                    {"type": "function", "function": Functions.get_archived_email_designs_JSON},
                    {"type": "function", "function": Functions.get_contact_csv_JSON},
                       ]
            )
            # Store the new assistant.id in .env
            #dotenv.set_key('.env', 'ASSISTANT_ID', assistant.id)
            ASSISTANT_ID = assistant.id
        else:
            assistant = self.client.beta.assistants.update(
                assistant_id=ASSISTANT_ID,
                name="Random Assistant",
                instructions=directions + "\n format responses in json and only the json portion of the response as a string.",
                model="gpt-4",
                tools=[
                    {"type": "code_interpreter"},
                    {"type": "function", "function": Functions.get_random_digit_JSON},
                    {"type": "function", "function": Functions.get_random_letters_JSON},
                    {"type": "function", "function": Functions.get_reports_JSON},
                    {"type": "function", "function": Functions.delete_campaigns_JSON},
                    {"type": "function", "function": Functions.list_campaigns_JSON},
                    {"type": "function", "function": Functions.schedule_email_campaign_JSON},
                    {"type": "function", "function": Functions.show_help_JSON},
                    {"type": "function", "function": Functions.update_contacts_JSON},
                    {"type": "function", "function": Functions.get_email_editor_JSON},
                    {"type": "function", "function": Functions.get_sample_email_text_JSON},
                    {"type": "function", "function": Functions.get_archived_reports_JSON},
                    {"type": "function", "function": Functions.get_archived_contact_lists_JSON},
                    {"type": "function", "function": Functions.get_archived_email_designs_JSON},
                    {"type": "function", "function": Functions.get_contact_csv_JSON},
                       ]
            )
        self.create_AI_thread()

    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating assistant thread...')
        self.thread = self.client.beta.threads.create()
        print(show_json(self.thread))
        with open(LOGFILE, 'a+') as f:
            f.write(f'# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread.id}\n\n')

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
            new_messages = self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc", after=self.message.id)
            response = list()
            with open(LOGFILE, 'a+') as f:
                f.write('\n**Assistant**:\n')
                for m in new_messages:
                    msg = m.content[0].text.value
                    #print()
                    #print(msg)
                    f.write(msg)
                    response.append(msg)
                f.write('\n\n---\n')
            # Callback to GUI with list of messages added after the user message we sent
            #return chatgpt_parse_response(''.join(response))
            return str(response).replace('```json', '').replace('```', '').replace('\\n', '')

    def send_message(self, message_text: str):
        """
        Send a message to the assistant.

        Parameters
        ----------
        """
        self.message = self.client.beta.threads.messages.create(self.thread.id,
                                                role = "user",
                                                content = message_text + " " + chatgpt_parse_date(message_text))
        print('\nSending:\n' + show_json(self.message))
        self.run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=ASSISTANT_ID)
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')


if __name__ == '__main__':
    #AI.send_message("give me a random number to include in my subject name")

    #AI = Assistant()
    #AI.send_message("List campaigns")
    #print(AI.wait_on_run())

    #AI = Assistant()
    #AI.send_message("Delete campaigns: 20243103-E3-Campaign1, 20243104")
    #print(AI.wait_on_run())

    #AI = Assistant()
    #AI.send_message("return 3 random letters.")
    #print(AI.wait_on_run())

    #AI = Assistant()
    #AI.send_message("delete the campaigns. campaigns: [20243103-E3-Campaign1, 20243103-E3-Campaign1,]")
    #print(AI.wait_on_run())

    #AI = Assistant()
    #AI.send_message("generate report")
    #print(AI.wait_on_run())

    AI = Assistant()
    AI.send_message("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign tomorrow")
    print(AI.wait_on_run())
    AI = Assistant()
    AI.send_message("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign this friday")
    print(AI.wait_on_run())
    #"emails"
    #"subject"
    #"scheduledAt"
    #"sender_name"
    #"test"

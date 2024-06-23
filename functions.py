#!/usr/bin/env python3.11
import shutil
from CoreService import main
from openai import OpenAI
import os
from datetime import datetime,timezone
import json
from flask import Flask, jsonify, request, render_template
from functools import wraps
from gen_report import initiate
from BrevoSend  import build_campaign, return_campaign_files, delete_campaign_files
from BrevoWorkflow import adhoc_build_campaign
from BrevoUpdateContactList  import brevo_load_contacts, main as update_contact_list
from BrevoBounceList import main as gen_bounce_list
import string
import random


OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
fqdn = "e3.ldmg.org"


def copy_contacts(file_name):
    shutil.copy("/var/www/html/uploads/user_contacts.csv", file_name)


def current_date():
    # Get the current date and time in UTC
    current_gmt_datetime = datetime.now(timezone.utc)
    # Format the date as YYYY-MM-DD
    formatted_date_gmt = current_gmt_datetime.strftime('%Y-%m-%d')
    return formatted_date_gmt


def chatgpt_parse_date(phrase):
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


def create_email(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Create the text for a sample email with the following requirements: '{phrase}'"}
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
          {"role": "user", "content": f"Extract the text here that represents a file name and convert to a purely a string and only the file name as a string. Do not return as markup."}
      ]
    )

    return response.choices[0].message.content.strip()


class Functions:
    def list_campaigns():
        campaign_files = return_campaign_files()
        if campaign_files:
            return campaign_files
        else:
            return "No campaigns currently scheduled."

    list_campaigns_JSON = {
        "name": "list_campaigns",
        "description": "list campaigns",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_random_digit():
        return random.randint(0,9)

    get_random_digit_JSON = {
        "name": "get_random_digit",
        "description": "Get a random digit",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_random_letters(count: int, case_sensitive: bool = False):
        return ''.join(random.choices(string.ascii_letters if case_sensitive else string.ascii_uppercase, k=count))

    get_random_letters_JSON = {
        "name": "get_random_letters",
        "description": "Get a string of random letters",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of letters to return"},
                "case_sensitive": {"type": "boolean", "description": "Whether to include lower-case letters.  Default only returns upper-case letters."}
            },
            "required": ["count"]
        }
    }

    def get_sample_email_text(email_requirements: str):
        #return "sample email text response"
        return create_email(email_requirements)

    get_sample_email_text_JSON = {
        "name": "get_sample_email_text",
        "description": "Create the text for sample email.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_requirements": {"type": "string", "description": "The requirements for the email that the user describes."}
                },
        }
    }

    def get_email_editor():
        return "Use the email editor at https://e3.ldmg.org/uploads/tiny-mice.html"

    get_email_editor_JSON = {
        "name": "get_email_editor",
        "description": "Return the link the the email editor to the user.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_contact_csv():
        return "Download contacts CSV doc here: https://docs.google.com/spreadsheets/d/1rwtospaUv6FBfYn9YYXNktJWUGxhGHJyqY_zWB9RWmY/edit?usp=sharing"

    get_contact_csv_JSON = {
        "name": "get_contact_csv",
        "description": "Return the link for the contact csv.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_reports():
        return "View the report at https://e3.ldmg.org/api/results"

    get_reports_JSON = {
        "name": "get_reports",
        "description": "Get the latest reports, get the latest report link,  or generate report and present ink to the user.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_archived_reports():
        return "View archived reports at https://e3.ldmg.org/uploads/reports"

    get_archived_reports_JSON = {
        "name": "get_archived_reports",
        "description": "Get archived reports, get the archived report link.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_archived_bounce_lists():
        return "View archived bounce lists at https://e3.ldmg.org/uploads/bounce_lists"

    get_archived_bounce_lists_JSON = {
        "name": "get_archived_bounce_lists",
        "description": "Get archived bounce lists, get the archived bounce lists link.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }


    def get_archived_contact_lists():
        return "View archived contact lists at https://e3.ldmg.org/uploads/contacts"

    get_archived_contact_lists_JSON = {
        "name": "get_archived_contact_lists",
        "description": "Get archived contacts lists, get the archived contact lists link.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_archived_email_designs():
        return "View archived email designs at https://e3.ldmg.org/uploads/email_designs"

    get_archived_email_designs_JSON = {
        "name": "get_archived_email_designs",
        "description": "Get archived email designs, get the archived email designs link.",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }


    def show_help():
        __help = [
                "Create a campaign with the subject 'Sample campaign' and send it on 5/19/2024",
                "List scheduled campaigns",
                "Create a sample email about teachers attending a training event, make it heart felt and inspiring.",
                "Delete campaign(s) 'A copy and pasted campaign name list of campaign names'",
                "Show report link",
                "Show contact csv link",
                "Show email editor link",
                "Show report archives link",
                "Show bounce list archives link",
                "Show email design archives link",
                "Show contact list archives link",
                "Help",
                ]
        return __help

    show_help_JSON = {
        "name": "show_help",
        "description": "Show help",
        "parameters": {
            #"type": "object",
            #"properties": {
            #    "help": {"type": "string", "description": "Show help to show what are some examples of what the assistant can do."},
            #},
            #"required": ["campaigns"]
        }
    }


    def update_contacts(message):
        return update_contact_list()

    update_contacts_JSON = {
        "name": "update_contacts",
        "description": "when the user request to Update contacts. Add contacts. Upload contacts.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "description": "Update contacts. Add contacts. Upload contacts."},
            },
            #"required": ["campaigns"]
        }
    }


    def delete_campaigns(campaigns: object):
        return delete_campaign_files(campaigns)
        #return "OK"

    delete_campaigns_JSON = {
        "name": "delete_campaigns",
        "description": "Delete campaigns",
        "parameters": {
            "type": "object",
            "properties": {
                "campaigns": {"type": "string", "description": "A list of campaign names provided by the user. Get the campaign names from the users message then provide them as a json list to the function."},
            },
            "required": ["campaigns"]
        }
    }


    #def copy_contacts(file_name):
    #    shutil.copy("/var/www/html/uploads/user_contacts.csv", file_name)


    def schedule_email_campaign(subject, sender_name, scheduledAt, emails=None, test="yes"):
        #if emails:
        #    brevo_load_contacts(adhoc_contacts=emails)
        schedule_date = chatgpt_parse_date(scheduledAt)
        if (subject and scheduledAt):
            data = {
                    "subject": subject,
                    "sender_name": sender_name,
                    "scheduledAt": schedule_date,
                    "emails" : emails,
                    "test": test,
                    }
            #if build_campaign(data):

            # Copy user uploaded contacts to the correct location
            copy_contacts(f'/var/www/html/uploads/contacts/{schedule_date}-E3-Campaign.csv')
            if os.path.exists(f'/var/www/html/uploads/contacts/{schedule_date}-E3-Campaign.csv'):
                print("File exists, continuing...")
                adhoc_build_campaign(data)
                return "Campaign scheduled"
            else:
                return "Error: You did not upload your contacts"

    schedule_email_campaign_JSON = {
        "name": "schedule_email_campaign",
        "description": "Send or schedule campaign",
        "parameters": {
            "type": "object",
            "properties": {
                "emails": {"type": "string", "description": "A list of emails that the user would like to use to send the email to. This gets added to the standard email list."},
                "subject": {"type": "string", "description": "The subject that the user would like to use in the email."},
                "scheduledAt": {"type": "string", "description": f"Campaign scheduling time."},
                "sender_name": {"type": "string", "description": "The name of the email campaign sender."},
                "test": {"type": "string", "description": "Determine whether this campaign schedule is test or not. By default if not set make this set to yes. If the user want to run a real campaign set to no."},
            },
            "required": ["subject", "sender_name", "scheduledAt"]
        }
    }


if __name__ == '__main__':
    print(chatgpt_parse_date("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign today"))
    print(chatgpt_parse_date("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign this friday"))

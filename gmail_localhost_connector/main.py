#!/usr/bin/python3.11

__created__ = "18.03.2023"
__last_update__ = ""
__author__ = "https://github.com/pyautoml"

"""
This is a simple connector to Gmail mailbox from a localhost application.
It will be supported by additional security classes responsible for validating
email meatadata and generating analytical reports.

Project current status: [ongoing]

Gmail API links:
    https://console.cloud.google.com/apis/dashboard
    https://console.cloud.google.com/apis/credentials
    https://console.cloud.google.com/apis/api/gmail.googleapis.com

Steps:
1. Register a new application connected to your Gmail account.
2. Include OAuth 2.0 client identifiers. Ensure "gmail.modify" permission is added.
3. Run main.py to automatically generate a token.pickle file.
4. Upon the initial run, manually grant privileges (allow connection) to your local application.
   Subsequent authentications will be handled using the existing token.
"""

import os
import json
import html
import pickle
import base64
import argparse
from patterns import patterns
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from security_validation import GmailContentSecurity
from google_auth_oauthlib.flow import InstalledAppFlow




class AbstractEmail(ABC):
    @abstractmethod
    def connect(self):
        pass


class Gmail(AbstractEmail):
    def __init__(
        self, token_file: str, credentias_file: str, console_messages: bool = False
    ) -> None:
        self.name = "Gmail"
        self.token_file = token_file
        self.console_messages = console_messages
        self.credentias_file = credentias_file
        self.scopes = ["https://www.googleapis.com/auth/gmail.modify"]

    def connect(self):
        if not os.path.exists(self.token_file):
            self.token_file = os.path.abspath(
                os.path.join(os.path.dirname(__file__), self.token_file)
            )
            if not os.path.exists(self.token_file):
                self.credentials = None
            else:
                self.credentials = self.load_tokens()
        else:
            self.credentials = self.load_tokens()

        try:
            if not self.credentials or not self.credentials.valid:
                if (
                    self.credentials
                    and self.credentials.expired
                    and self.credentials.refresh_token
                ):
                    self.credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentias_file, self.scopes
                    )
                    self.credentials = flow.run_local_server(port=0)
                self.save_tokens()
            self.service = build("gmail", "v1", credentials=self.credentials)
            if self.console_messages:
                print(f"Connected to {self.name}.", flush=True)
        except Exception as e:
            raise Exception(f"Error in credentials validations: {e}")

    def save_tokens(self) -> None:
        try:
            with open(self.token_file, "wb") as file:
                pickle.dump(self.credentials, file)
            if self.console_messages:
                print("Saved credentials.", flush=True)
        except Exception as e:
            raise Exception(f"Cannot save token: {e}")

    def load_tokens(self) -> pickle:
        try:
            with open(self.token_file, "rb") as file:
                return pickle.load(file)
        except Exception as e:
            raise Exception(f"Cannot load token: {e}")

    def retrieve_emails(self, custom_filter: dict = None) -> list:
        try:
            if custom_filter:
                result = (
                    self.service.users()
                    .settings()
                    .filters()
                    .create(userId="me", body=custom_filter)
                    .execute()
                )
            else:
                result = (
                    self.service.users()
                    .messages()
                    .list(userId="me", q="is:unread in:inbox")
                    .execute()
                )
            return result.get("messages")
        except HttpError as e:
            raise HttpError(f"Connection error: {e}")
        except Exception as e:
            raise Exception(f"Error in retrieving emails: {e}")

    def get_metadata(self, message: dict) -> dict:
        return {"example": ""}  # TODO

    def get_message(
        self,
        message_id: str,
        raw_message: bool = False,
        only_payload: bool = False,
        only_metadata: bool = False,
        only_headers: bool = False,
    ) -> dict:
        try:
            message = (
                self.service.users().messages().get(userId="me", id=message_id).execute()
            )
        except HttpError as e:
            raise HttpError(f"Gmail API connection error for message id '{message_id}': {e}")
        except Exception as e:
            raise Exception(f"Cannot get message of id '{message_id}' : {e}")
        
        try:
            if message:
                if raw_message:
                    return message
                elif only_payload:
                    return message["payload"]
                elif only_metadata:
                    return self.get_metadata(message)
                elif only_headers:
                    headers = {}
                    for element in message["payload"]["headers"]:
                        headers[element["name"]] = element["value"]
                    return headers
                else:
                    return message
        except KeyError as e:
            raise KeyError(f"Missing key(s) in {self.name} for message of id '{message_id}': {e}")
        except Exception as e:
            raise Exception(f"Error in retrieving data from {self.name} message of id '{message_id}': {e}")

    def get_headers(self, message: dict) -> dict:
        """ Separate function for extracting headers from the message. """

        try:
            if "payload" in message.keys():
                if "headers" in message["payload"].keys():
                    return message["payload"]["headers"]
            elif "headers" in message.keys():
                return message["headers"]
        except KeyError as e:
            raise KeyError(f"Error in retrieving payload headers: {e}")
        except Exception as e:
            raise Exception(f"Error in retrieving payload headers: {e}")
          

    def filter_example(self) -> dict:
      """ Filter query example template. """
      
        return {
            "id": "unique_filter_id",
            "criteria": {"from": "example@gmail.com", "hasAttachment": True},
            "action": {"addLabelIds": ["Label_1"], "removeLabelIds": ["INBOX"]},
            "priority": 1,
            "status": "active",
            "executionTime": "immediate",
            "conditions": {"size": "larger:5M", "negate": False},
            "actionOnMultipleMessages": {"archive": True, "markAsImportant": True},
        }


# usage example
def main():
    gmail = Gmail(
        token_file="./credentials/token.pickle",
        credentias_file="./credentials/credentials.json",
        console_messages=True,
    )
    gmail.connect()
    messages = gmail.retrieve_emails()
    headers = gmail.get_message(message_id=messages[0]["id"], only_headers=True)
    # security = GmailContentSecurity()


if __name__ == "__main__":
    main()

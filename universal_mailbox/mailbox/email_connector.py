#!/usr/bin/python3.11

__created__ = "30.10.2023"
__last_update__ = "01.11.2023"
__author__ = "https://github.com/pyautoml"

import gc
import os
import sys
import json
import imaplib
# from logger import logger
from typing import Any, List
from utils import absolute_path, load_json_data


class EmailConnector:
    _instance: Any = None

    def __init__(
        self,
        mailbox: str,
        email_provider: str,
        console_messages: bool = False,
        settings_file_abs_path: str = None,
    ) -> None:
        self._instancebox = mailbox
        self._set_email_provider(email_provider)
        self._console_messages = console_messages

        if settings_file_abs_path:
            self._settings_file_abs_path = settings_file_abs_path

    def __new__(cls, *args, **kwargs):
        """
        Create singleton connector.

        Parameters
        -----------
        cls - class instance
        *args - objects as list
        ** kwargs - objects as dict
        """

        try:
            if cls._instance is None:
                cls._instance = super(cls.__class__, cls).__new__(cls)
            return cls._instance
        except Exception as e:
            # logger.exception(f"{e}")
            sys.exit(1)

    def __str__(self) -> str:
        return self._instancebox

    @classmethod
    def _forbidden_access(cls) -> List[str]:
        """Data that should not be accessible to users."""

        return ["_load_settings", "_forbidden_access", "_settings_file_abs_path"]

    @classmethod
    def __setattr__(cls, attribute: str, value: Any) -> None:
        """
        Set class attributes. Disallow to add new attributes.

        Parameters
        -----------
        attribute (str): class object's attribute
        value (str): attribute's value
        """

        if attribute == "_instancebox":
            cls._instancebox = value
        elif attribute == "_instance":
            cls._instance = "_instance"
        elif attribute == "_connection":
            cls._connection = value
        elif attribute == "_console_messages":
            cls._console_messages = value
        elif attribute == "_email_provider":
            cls._email_provider = value
        elif attribute == "_settings_file_abs_path":
            cls._settings_file_abs_path = value
        else:
            pass

    def __dir__(self) -> list:
        """Remove confidential data from class dictionary."""

        dirs = super().__dir__()
        forbidden = super()._forbidden_access()
        new_dir = [name for name in dirs if name not in forbidden]
        return sorted(new_dir)

    def _set_email_provider(self, email_provider: str) -> None:
        """
        Choose email provider imap server.

        Parameters
        ----------
        email_provider (str): imap server key name, for example: gmail, outlook, aol.
        """

        try:
            settings_path = self._settings_file_abs_path
        except:
            settings_path = absolute_path(
                os.path.join("..", "configuration/imap_servers.json")
            )
        try:
            with open(settings_path, "r") as json_file:
                providers = json.load(json_file)
        except Exception as e:
            print(e)
            # logger.exception("Settings directory does not exist: {e}")
            sys.exit(1)

        email_provider = email_provider.lower()
        if email_provider in providers.keys():
            self._email_provider = providers[email_provider]
        else:
            print(e)
            # logger.exception(f"No suich provider registered. PRegistered providers: {providers.keys()}")
            sys.exit(1)

    def _load_settings(self, settings: str = None) -> dict:
        try:
            if not settings:
                with open(
                    absolute_path(os.path.join("..", "configuration/settings.json")),
                    "r",
                ) as json_file:
                    settings = json.load(json_file)[self._instancebox]
                    settings["imap_server"] = self._email_provider
                expected_keys = [
                    "email_address",
                    "email_password",
                    "imap_server",
                    "imap_port",
                ]
                for key in expected_keys:
                    if key not in settings.keys():
                        print(e)
                        # logger.exception(f"Missing confoguration key: {key}")
                        sys.exit(1)
                return settings
            else:
                return load_json_data(settings)
        except Exception as e:
            print(e)
            # logger.exception(f"{e}")
            sys.exit(1)

    def _connect(self, settings: str = None) -> None:
        """Connect to the specified email account."""

        if not settings:
            try:
                settings = self._load_settings()
            except Exception as e:
                print(e)
                # logger.exception(f"{e}")
                sys.exit(1)
        else:
            settings = self._load_settings(settings)

        try:
            self._connection = imaplib.IMAP4_SSL(
                settings["imap_server"], settings["imap_port"]
            )
            self._connection.login(
                settings["email_address"], settings["email_password"]
            )
            del settings
            gc.collect()

            if self._console_messages:
                print(f"Connected to: {str(self)}", flush=True)
        except KeyError as e:
            print(e)
            # logger.exception(f"{e}")
            sys.exit(1)

    def _disconnect(self):
        """Close current email connection and log out."""
        try:
            self._connection.logout()
        except Exception as e:
            print(e)
            # logger.exception(f"Error when trying to log off: {e}")
            try:
                self._connection.close()
            except Exception as e:
                # logger.exception(f"Error when trying to log off: {e}")
                print(e)
                sys.exit(1)
        finally:
            if self._console_messages:
                print(f"Disconnected from: {self._instancebox}")

#!/usr/bin/python3.11

__created__ = "01.11.2023"
__last_update__ = "02.11.2023"
__author__ = "https://github.com/pyautoml"


import gc
import sys
import email
import imaplib
from copy import deepcopy
# from logger import logger
from typing import Any, List
from utils import absolute_path
from functools import lru_cache
from email.parser import HeaderParser
from dataclasses import dataclass, field
from email_connector import EmailConnector


@dataclass
class EmailParser:
    _mail: EmailConnector
    _filter_tags: dict = field(
        default_factory=lambda: {
            "body": "BODY",
            "by_keyword": "KEYWORD",
            "subject": "SUBJECT",
            "mail_to": "TO",
            "mail_from": "FROM",
            "since": "SINCE",
            "before": "BEFORE",
            "cc": "CC",
            "bcc": "BCC",
            "user_agent": "USER",
            "header_message_id": "HEADER Message-ID",
            "seen": "SEEN",
            "unseen": "UNSEEN",
            "answered": "ANSWERED",
            "unanswered": "UNANSWERED",
            "deleted": "DELETED",
            "flagged": "FLAGGED",
            "custom_search": "KEYWORD",
            "high_priority": "HIGH",
            "low_priority": "LOW",
            "has_attachment": "HASATTACH",
            "attachment_smaller_than": "SMALLER",
            "attachment_larger_than": "LARGER",
        }
    )

    def _set_filter(
        self,
        body: str = None,
        by_keyword: str = None,
        subject: str = None,
        mail_from: str = None,
        mail_to: str = None,
        since: str = None,
        before: str = None,
        cc: str = None,
        bcc: str = None,
        user_agent: str = None,
        header_message_id: str = None,
        seen: bool = None,
        unseen: bool = None,
        answered: bool = None,
        unanswered: bool = None,
        deleted: bool = None,
        flagged: bool = None,
        custom_search: str = None,
        high_priority: bool = None,
        low_priority: bool = None,
        has_attachment: bool = None,
        attachment_smaller_than: int = None,
        attachment_larger_than: int = None,
    ) -> dict:
        requested_filter_parameters = deepcopy(self._filter_tags)
        requested_filter_parameters["body"] = (
            f"({self._filter_tags['body']} '{body}')" if body else None
        )
        requested_filter_parameters["by_keyword"] = (
            f"({self._filter_tags['by_keyword']} '{by_keyword}')"
            if by_keyword
            else None
        )
        requested_filter_parameters["subject"] = (
            f"({self._filter_tags['subject']} '{subject}')" if subject else None
        )
        requested_filter_parameters["mail_from"] = (
            f"({self._filter_tags['mail_from']} '{mail_from}')" if mail_from else None
        )
        requested_filter_parameters["mail_to"] = (
            f"({self._filter_tags['mail_to']} '{mail_to}')" if mail_to else None
        )
        requested_filter_parameters["since"] = (
            f"({self._filter_tags['since']} '{since}')" if since else None
        )
        requested_filter_parameters["before"] = (
            f"({self._filter_tags['before']} '{before}')" if before else None
        )
        requested_filter_parameters["cc"] = (
            f"({self._filter_tags['cc']} '{cc}')" if cc else None
        )
        requested_filter_parameters["bcc"] = (
            f"({self._filter_tags['bcc']} '{bcc}')" if bcc else None
        )
        requested_filter_parameters["user_agent"] = (
            f"({self._filter_tags['user_agent']} '{user_agent}')"
            if user_agent
            else None
        )
        requested_filter_parameters["header_message_id"] = (
            f"({self._filter_tags['header_message_id']} '{header_message_id}')"
            if header_message_id
            else None
        )
        requested_filter_parameters["seen"] = (
            f"({self._filter_tags['seen']})" if seen else None
        )
        requested_filter_parameters["unseen"] = (
            f"({self._filter_tags['unseen']})" if unseen else None
        )
        requested_filter_parameters["answered"] = (
            f"({self._filter_tags['answered']})" if answered else None
        )
        requested_filter_parameters["unanswered"] = (
            f"({self._filter_tags['unanswered']})" if unanswered else None
        )
        requested_filter_parameters["deleted"] = (
            f"({self._filter_tags['deleted']})" if deleted else None
        )
        requested_filter_parameters["flagged"] = (
            f"({self._filter_tags['flagged']})" if flagged else None
        )
        requested_filter_parameters["custom_search"] = (
            f"({self._filter_tags['custom_search']} '{custom_search}')"
            if custom_search
            else None
        )
        requested_filter_parameters["high_priority"] = (
            f"({self._filter_tags['high_priority']})" if high_priority else None
        )
        requested_filter_parameters["low_priority"] = (
            f"({self._filter_tags['low_priority']})" if low_priority else None
        )
        requested_filter_parameters["has_attachment"] = (
            f"({self._filter_tags['has_attachment']})" if has_attachment else None
        )
        requested_filter_parameters["attachment_smaller_than"] = (
            f"({self._filter_tags['attachment_smaller_than']} {attachment_smaller_than})"
            if attachment_smaller_than
            else None
        )
        requested_filter_parameters["attachment_larger_than"] = (
            f"({self._filter_tags['attachment_larger_than']} {attachment_larger_than})"
            if attachment_larger_than
            else None
        )

        cleaned_parameters = ""
        for value in requested_filter_parameters.values():
            if value:
                cleaned_parameters += value + " "
        del requested_filter_parameters
        gc.collect()
        return cleaned_parameters.rstrip()

    def _get_email(self, mailbox: str = "Inbox", filter: dict = None) -> List[list]:
        """TODO"""

        self._mail.select(mailbox)
        if not filter:
            result, data = self._mail.search(None, "ALL")
        else:
            pass

        message_ids = data[0].split()

        for message_id in message_ids:
            result, message_data = self._mail.fetch(message_id, "(RFC822)")
            raw_email = message_data[0][1]
            message = email.message_from_string(raw_email)

    @lru_cache(maxsize=100, typed=True)
    def _parse_email(self, raw_email) -> List[list]:
        try:
            message = self._email.message_from_bytes(raw_email)
            message_body = ""
            attachments = []

            if message.is_multipart():
                for part in message.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if part.get_payload():
                        if (
                            not content_disposition
                            or not content_disposition.startswith("attachment")
                        ):
                            message_body += part.get_payload(decode=True).decode(
                                "utf-8", errors="ignore"
                            )
                        else:
                            attachments.append(
                                (part.get_filename(), part.get_payload(decode=True))
                            )

            # print("Message Body:", message_body)
            # print("Attachments:", attachments)

        except Exception as e:
            print(f"An error occurred while processing the email: {e}")

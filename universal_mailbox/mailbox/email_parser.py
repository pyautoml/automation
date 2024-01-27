#!/usr/bin/python3.11

__created__ = "01.11.2023"
__last_update__ = "05.11.2023"
__author__ = "https://github.com/pyautoml"

import re
import gc
import os
import sys
import email
import emoji
from copy import deepcopy
from logger import logger
from typing import Any, List
from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache
from utils import absolute_path
from email.parser import Parser
from typing import Final, Generator
from email.header import decode_header
from dataclasses import dataclass, field
from email_connector import EmailConnector


@dataclass
class EmailParser:
    _mail: EmailConnector
    _parser: Parser = Parser()
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
    _accepted_file_extensions: Final[list] = field(
        default_factory=lambda: [
            ".jpg",
            ".png",
            ".gif",
            ".txt" ".csv",
            ".pdf",
            ".xlsx",
            ".doc",
            ".jpeg",
            ".pptx",
            ".docx",
        ]
    )

    _blocked_file_extensions: Final[list] = field(
        default_factory=lambda: [".7z", ".zip", ".tar", ".gzip"]
    )

    def __hash__(self):
        return hash(tuple())

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
        possible_values = [
            body,
            by_keyword,
            subject,
            mail_to,
            mail_from,
            since,
            before,
            cc,
            bcc,
            user_agent,
            header_message_id,
            seen,
            unseen,
            answered,
            unanswered,
            deleted,
            flagged,
            custom_search,
            high_priority,
            low_priority,
            has_attachment,
            attachment_smaller_than,
            attachment_larger_than,
        ]
        boolean_values = [
            "seen",
            "unseen",
            "answered",
            "unanswered",
            "deleted",
            "flagged",
            "high_priority",
            "low_priority",
            "has_attachment",
        ]
        int_values = ["attachment_smaller_than", "attachment_larger_than"]

        for key, value in zip(self._filter_tags.keys(), possible_values):
            if key in boolean_values:
                requested_filter_parameters[key] = (
                    f"{self._filter_tags[key]}" if value else None
                )
            elif key in int_values:
                requested_filter_parameters[key] = (
                    f"{self._filter_tags[key]} {value}" if value else None
                )
            else:
                requested_filter_parameters[key] = (
                    f'{self._filter_tags[key]} "{value}"' if value else None
                )

        cleaned_parameters = ""
        for value in requested_filter_parameters.values():
            if value:
                cleaned_parameters += value + " "
        cleaned_parameters = cleaned_parameters[:-1]

        del requested_filter_parameters
        gc.collect()
        return f"({cleaned_parameters.rstrip()})"

    def _decode_headers(self, data: str) -> str:
        try:
            subject, charset = decode_header(data)[0]
            return subject if charset is None else subject.decode(charset)
        except:
            return data

    def _parse_timestamp(self, date: str) -> str:
        parsed_date = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    def _headers(self, email, only_basic_headers: bool) -> dict:
        if only_basic_headers:
            return {
                "Body": None,
                "Subject": email["subject"],
                "From": email["from"],
                "To": email["to"],
                "CC": email["cc"],
                "BCC": email["bcc"],
                "Date": email["date"],
                "Reply-To": email["reply-to"],
                "Message-ID": email["message-id"],
            }
        else:
            return {
                "Body": None,
                "Subject": email["subject"],
                "From": email["from"],
                "To": email["to"],
                "CC": email["cc"],
                "BCC": email["bcc"],
                "Date": email["date"],
                "Reply-To": email["reply-to"],
                "Message-ID": email["message-id"],
                "In-Reply-To": email["in-reply-to"],
                "References": email["references"],
                "Content-Type": email["content-type"],
                "MIME-Version": email["mime-version"],
                "Content-Transfer-Encoding": email["content-transfer-encoding"],
                "Content-Disposition": email["content-disposition"],
                "Content-Description": email["content-description"],
                "Content-Language": email["content-language"],
                "Content-Location": email["content-location"],
                "Received": email["received"],
                "X-Priority": email["x-priority"],
                "X-Mailer": email["x-mailer"],
                "X-Original-Sender": email["x-original-sender"],
                "X-Sender": email["x-sender"],
                "X-MS-TNEF-Correlator": email["x-ms-tnef-correlator"],
                "Thread-Index": email["thread-index"],
            }

    def _separate_sender_and_email(self, data: str) -> dict:
        try:
            sender, email = data.split("<")
            return sender.strip(), email[:-1].strip()
        except:
            return data

    def _save_attachment_locally(
        self,
        email_timestamp: str,
        file_name: str,
        attachment: Any,
        local_path: str = None,
    ) -> None:
        if not local_path:
            if not os.path.exists(absolute_path("attachments")):
                os.mkdir(absolute_path("attachments"))
            local_path = absolute_path("attachments")
        elif not os.path.exists(local_path):
            new_path = absolute_path(local_path)
            if os.path.exists(new_path):
                local_path = new_path
            else:
                os.mkdir(absolute_path("attachments"))
                local_path = absolute_path("attachments")

        try:
            with open(f"{local_path}/{email_timestamp}_{file_name}", "wb") as file:
                file.write(attachment)
        except Exception as e:
            logger.critical(f"Cannot save attachment: {e}")
            sys.exit(1)

    def _find_attachments(
        self,
        email_message,
        email_timestamp: str,
        save_attachment: bool = False,
        local_path: str = None,
        return_attachments: bool = False,
    ) -> [list | None]:
        attachments = []
        for part in email_message.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get("Content-Disposition") is not None:
                filename = part.get_filename()
                if filename:
                    attachment_data = part.get_payload(decode=True)
                    file_extension = os.path.splitext(filename)[1].lower()
                    if file_extension in self._accepted_file_extensions:
                        if save_attachment:
                            self._save_attachment_locally(
                                email_timestamp=email_timestamp,
                                file_name=f"{filename}",
                                attachment=attachment_data,
                                local_path=local_path,
                            )
                        attachments.append(attachment_data)
                    elif file_extension in self._blocked_file_extensions:
                        logger.critical("Potentially malicious file blocked!: {file_name}")
                        return None
                    else:
                        logger.critical("Unsupported file extension: {file_name}")
                        return None
        if return_attachments:
            return attachments
        else:
            return None

    def _replace_html_tags_with_links(self, text: str) -> str:
        links = re.findall(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            text,
        )
        for link in links:
            text = (
                text.replace(f'<a href="{link}">', link)
                .replace(">", "")
                .replace("<", "")
            )
        return text

    def _replace_emojis_with_text(self, text: str) -> str:
        emojis = [
            match.group()
            for match in re.finditer(
                r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001F004-\U0001F0CF\U0001F170-\U0001F251\U0001F004-\U0001F0CF\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U0001F004-\U0001F0CF\U0001F170-\U0001F251]+",
                text,
                re.UNICODE,
            )
        ]
        for e in emojis:
            text = text.replace(e, emoji.demojize(e))
        return text

    def _extract_email_body(self, email_message):
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if content_type == "text/plain" or content_type == "text/html":
                        charset = part.get_content_charset()
                        email_text = part.get_payload(decode=True).decode(
                            charset, "ignore"
                        )

                        if content_type == "text/html":
                            soup = BeautifulSoup(email_text, "html.parser")
                            email_text = soup.get_text()
                        body += email_text
        return body

    @lru_cache(maxsize=100, typed=True)
    def _get_emails(
        self,
        mailbox: str = "Inbox",
        emoji_support: bool = True,
        clean_body_text: bool = False,
        format_datetime: bool = False,
        return_attachments: bool = False,
        save_attachments: bool = False,
        save_attachments_path: str = None,
        search_filter: str = "ALL",
        only_basic_headers: bool = True,
        separate_sender_email: bool = False,
    ) -> Generator:
        self._mail._select(mailbox=mailbox)
        data = self._mail._search(search_filter)
        message_ids = data[0].split()

        for message_id in message_ids:
            _, message_data = self._mail._fetch(message_id)
            email_message = email.message_from_bytes(message_data[0][1])
            email_body = self._extract_email_body(email_message)
            headers = self._headers(
                email_message, only_basic_headers=only_basic_headers
            )

            decoded_data = {}
            for key, value in headers.items():
                decoded_data[key] = self._decode_headers(value)

            if emoji_support:
                email_body = self._replace_emojis_with_text(email_body)

            decoded_data["Message-ID"] = str(decoded_data["Message-ID"])[1:-1]

            if format_datetime:
                decoded_data["Date"] = self._parse_timestamp(decoded_data["Date"])

            if separate_sender_email:
                if decoded_data["From"]:
                    try:
                        from_sender, from_email = self._separate_sender_and_email(
                            decoded_data["From"]
                        )
                        decoded_data["From"] = from_sender
                        decoded_data["From Email"] = from_email
                    except:
                        pass

                if decoded_data["CC"]:
                    try:
                        cc_sender, cc_email = self._separate_sender_and_email(
                            decoded_data["CC"]
                        )
                        decoded_data["CC"] = cc_sender
                        decoded_data["CC Email"] = cc_email
                    except:
                        pass

                if decoded_data["BCC"]:
                    try:
                        cc_sender, cc_email = self._separate_sender_and_email(
                            decoded_data["BCC"]
                        )
                        decoded_data["BCC"] = cc_sender
                        decoded_data["BCC Email"] = cc_email
                    except:
                        pass

                if decoded_data["Reply-To"]:
                    try:
                        reply_sender, reply_email = self._separate_sender_and_email(
                            decoded_data["Reply-To"]
                        )
                        decoded_data["Reply-To"] = reply_sender
                        decoded_data["Reply-To Email"] = reply_email
                    except:
                        pass

                if decoded_data["To"]:
                    try:
                        to_sender, to_email = self._separate_sender_and_email(
                            decoded_data["To"]
                        )
                        decoded_data["To"] = to_sender
                        decoded_data["To Email"] = to_email
                    except:
                        pass

            try:
                self._replace_html_tags_with_links(email_body)
            except:
                pass

            if clean_body_text:
                email_body = re.sub(r"\s+", " ", str(email_body))
                email_body = email_body.split("\n")
                decoded_data["Body"] = str(email_body[0]).lstrip().rstrip()
            else:
                decoded_data["Body"] = email_body
            decoded_data = {key: decoded_data[key] for key in sorted(decoded_data)}

            attachment_timestamp = (
                str(self._parse_timestamp(decoded_data["Date"]))
                .replace(" ", "_")
                .replace(":", "-")
                if not format_datetime
                else str(decoded_data["Date"]).replace(" ", "_").replace(":", "-")
            )

            attachments = self._find_attachments(
                email_message=email_message,
                email_timestamp=attachment_timestamp,
                save_attachment=save_attachments,
                local_path=save_attachments_path,
                return_attachments=return_attachments,
            )

            if return_attachments:
                yield decoded_data, attachments
            else:
                yield decoded_data, None

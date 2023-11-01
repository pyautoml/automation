#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

__created__ = "01.11.2023"
__last_update__ = "01.11.2023"
__author__ = "https://github.com/pyautoml"
__how_to__ = ["python -m unittest test.test_email_parser"]

import os
import gc
import atexit
import unittest
import tracemalloc
from utils import (
    run_makefile,
    absolute_path,
)
from email_parser import EmailParser
from email_connector import EmailConnector


class TestEmailParser(unittest.TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    atexit.register(run_makefile, "remove", path)

    def setUp(self) -> None:
        tracemalloc.start()
        self.connector = EmailConnector("your_user", email_provider="email_provider")
        self.parser = EmailParser(self.connector)

        self.comaprative_text = "compare"
        self.body = "body example"
        self.mail_to = "mail to example"
        self.unseen = True
        self.custom_search = "custom search example"
        self.bcc = "bcc example"
        self.mail_from = "mail from example"
        self.high_priority = True
        self.attachment_smaller_than = 1000
        self.expected_text_one = "(BODY 'body example') (TO 'mail to example') (UNSEEN) (KEYWORD 'custom search example')"
        self.expected_text_two = (
            "(FROM 'mail from example') (BCC 'bcc example') (HIGH) (SMALLER 1000)"
        )

    def tearDown(self) -> None:
        tracemalloc.stop()
        for item in self.__dir__():
            del item

    def test_positive_set_filter_chain(self) -> None:
        """Check if set_filter combined filters match expected string."""

        filter_chain_one = self.parser._set_filter(
            body=self.body,
            mail_to=self.mail_to,
            unseen=self.unseen,
            custom_search=self.custom_search,
        )

        filter_chain_two = self.parser._set_filter(
            bcc=self.bcc,
            mail_from=self.mail_from,
            high_priority=self.high_priority,
            attachment_smaller_than=self.attachment_smaller_than,
        )

        self.assertEqual(filter_chain_one, self.expected_text_one)
        self.assertEqual(filter_chain_two, self.expected_text_two)

    def test_negative_set_filter_chain(self) -> None:
        """Check if set_filter combined filters match expected string."""

        filter_chain_one = self.parser._set_filter(
            body=self.body,
            mail_to=self.mail_to,
            unseen=self.unseen,
            custom_search=self.custom_search,
        )

        filter_chain_two = self.parser._set_filter(
            bcc=self.bcc,
            mail_from=self.mail_from,
            high_priority=self.high_priority,
            attachment_smaller_than=self.attachment_smaller_than,
        )

        self.assertNotEqual(filter_chain_one, self.expected_text_one + ".")
        self.assertNotEqual(filter_chain_two, self.expected_text_two + ".")

    def test_positive_set_filter_single(self) -> None:
        """Chceck if set_filter return expected data."""

        filter_body = self.parser._set_filter(body=self.comaprative_text)
        self.assertEqual(f"(BODY '{self.comaprative_text}')", filter_body)

        filter_by_keyword = self.parser._set_filter(by_keyword=self.comaprative_text)
        self.assertEqual(f"(KEYWORD '{self.comaprative_text}')", filter_by_keyword)

        filter_subject = self.parser._set_filter(subject=self.comaprative_text)
        self.assertEqual(f"(SUBJECT '{self.comaprative_text}')", filter_subject)

        filter_mail_to = self.parser._set_filter(mail_to=self.comaprative_text)
        self.assertEqual(f"(TO '{self.comaprative_text}')", filter_mail_to)

        filter_mail_from = self.parser._set_filter(mail_from=self.comaprative_text)
        self.assertEqual(f"(FROM '{self.comaprative_text}')", filter_mail_from)

        filter_since = self.parser._set_filter(since=self.comaprative_text)
        self.assertEqual(f"(SINCE '{self.comaprative_text}')", filter_since)

        filter_before = self.parser._set_filter(before=self.comaprative_text)
        self.assertEqual(f"(BEFORE '{self.comaprative_text}')", filter_before)

        filter_cc = self.parser._set_filter(cc=self.comaprative_text)
        self.assertEqual(f"(CC '{self.comaprative_text}')", filter_cc)

        filter_bcc = self.parser._set_filter(bcc=self.comaprative_text)
        self.assertEqual(f"(BCC '{self.comaprative_text}')", filter_bcc)

        filter_user_agent = self.parser._set_filter(user_agent=self.comaprative_text)
        self.assertEqual(f"(USER '{self.comaprative_text}')", filter_user_agent)

        filter_header_message_id = self.parser._set_filter(
            header_message_id=self.comaprative_text
        )
        self.assertEqual(
            f"(HEADER Message-ID '{self.comaprative_text}')", filter_header_message_id
        )

        filter_seen = self.parser._set_filter(seen=True)
        self.assertEqual(f"(SEEN)", filter_seen)

        filter_unseen = self.parser._set_filter(unseen=True)
        self.assertEqual(f"(UNSEEN)", filter_unseen)

        filter_answered = self.parser._set_filter(answered=True)
        self.assertEqual(f"(ANSWERED)", filter_answered)

        filter_unanswered = self.parser._set_filter(unanswered=True)
        self.assertEqual(f"(UNANSWERED)", filter_unanswered)

        filter_deleted = self.parser._set_filter(deleted=True)
        self.assertEqual(f"(DELETED)", filter_deleted)

        filter_flagged = self.parser._set_filter(flagged=True)
        self.assertEqual(f"(FLAGGED)", filter_flagged)

        filter_custom_search = self.parser._set_filter(
            custom_search=self.comaprative_text
        )
        self.assertEqual(f"(KEYWORD '{self.comaprative_text}')", filter_custom_search)

        filter_high_priority = self.parser._set_filter(high_priority=True)
        self.assertEqual(f"(HIGH)", filter_high_priority)

        filter_low_priority = self.parser._set_filter(low_priority=True)
        self.assertEqual(f"(LOW)", filter_low_priority)

        filter_has_attachment = self.parser._set_filter(has_attachment=True)
        self.assertEqual(f"(HASATTACH)", filter_has_attachment)

        filter_attachment_smaller_than = self.parser._set_filter(
            attachment_smaller_than=self.comaprative_text
        )
        self.assertEqual(
            f"(SMALLER {self.comaprative_text})", filter_attachment_smaller_than
        )

        filter_attachment_larger_than = self.parser._set_filter(
            attachment_larger_than=self.comaprative_text
        )
        self.assertEqual(
            f"(LARGER {self.comaprative_text})", filter_attachment_larger_than
        )

    def test_negative_set_filter_single(self) -> None:
        """Chceck if set_filter return does not match xpected data."""

        filter_body = self.parser._set_filter(body=self.comaprative_text)
        self.assertNotEqual(f"(BODY '{self.comaprative_text}'.)", filter_body)

        filter_by_keyword = self.parser._set_filter(by_keyword=self.comaprative_text)
        self.assertNotEqual(f"(KEYWORD '{self.comaprative_text}'.)", filter_by_keyword)

        filter_subject = self.parser._set_filter(subject=self.comaprative_text)
        self.assertNotEqual(f"(SUBJECT '{self.comaprative_text}'.)", filter_subject)

        filter_mail_to = self.parser._set_filter(mail_to=self.comaprative_text)
        self.assertNotEqual(f"(TO '{self.comaprative_text}'.)", filter_mail_to)

        filter_mail_from = self.parser._set_filter(mail_from=self.comaprative_text)
        self.assertNotEqual(f"(FROM '{self.comaprative_text}'.)", filter_mail_from)

        filter_since = self.parser._set_filter(since=self.comaprative_text)
        self.assertNotEqual(f"(SINCE '{self.comaprative_text}'.)", filter_since)

        filter_before = self.parser._set_filter(before=self.comaprative_text)
        self.assertNotEqual(f"(BEFORE '{self.comaprative_text}'.)", filter_before)

        filter_cc = self.parser._set_filter(cc=self.comaprative_text)
        self.assertNotEqual(f"(CC '{self.comaprative_text}',)", filter_cc)

        filter_bcc = self.parser._set_filter(bcc=self.comaprative_text)
        self.assertNotEqual(f"(BCC '{self.comaprative_text}'.)", filter_bcc)

        filter_user_agent = self.parser._set_filter(user_agent=self.comaprative_text)
        self.assertNotEqual(f"(USER '{self.comaprative_text}'.)", filter_user_agent)

        filter_header_message_id = self.parser._set_filter(
            header_message_id=self.comaprative_text
        )
        self.assertNotEqual(
            f"(HEADER Message-ID '{self.comaprative_text}'.)", filter_header_message_id
        )

        filter_seen = self.parser._set_filter(seen=True)
        self.assertNotEqual(f"(SEEN.)", filter_seen)

        filter_unseen = self.parser._set_filter(unseen=True)
        self.assertNotEqual(f"(UNSEEN.)", filter_unseen)

        filter_answered = self.parser._set_filter(answered=True)
        self.assertNotEqual(f"(ANSWERED.)", filter_answered)

        filter_unanswered = self.parser._set_filter(unanswered=True)
        self.assertNotEqual(f"(UNANSWERED.)", filter_unanswered)

        filter_deleted = self.parser._set_filter(deleted=True)
        self.assertNotEqual(f"(DELETED.)", filter_deleted)

        filter_flagged = self.parser._set_filter(flagged=True)
        self.assertNotEqual(f"(FLAGGED.)", filter_flagged)

        filter_custom_search = self.parser._set_filter(
            custom_search=self.comaprative_text
        )
        self.assertNotEqual(
            f"(KEYWORD '{self.comaprative_text}'.)", filter_custom_search
        )

        filter_high_priority = self.parser._set_filter(high_priority=True)
        self.assertNotEqual(f"(HIGH.)", filter_high_priority)

        filter_low_priority = self.parser._set_filter(low_priority=True)
        self.assertNotEqual(f"(LOW.)", filter_low_priority)

        filter_has_attachment = self.parser._set_filter(has_attachment=True)
        self.assertNotEqual(f"(HASATTACH.)", filter_has_attachment)

        filter_attachment_smaller_than = self.parser._set_filter(
            attachment_smaller_than=self.comaprative_text
        )
        self.assertNotEqual(
            f"(SMALLER {self.comaprative_text}.)", filter_attachment_smaller_than
        )

        filter_attachment_larger_than = self.parser._set_filter(
            attachment_larger_than=self.comaprative_text
        )
        self.assertNotEqual(
            f"(LARGER {self.comaprative_text }.)", filter_attachment_larger_than
        )


if __name__ == "__main__":
    unittest.main()
    gc.collect()

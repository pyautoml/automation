#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

__created__ = "31.10.2023"
__last_uodate__ = "31.10.2023"
__author__ = "https://github.com/pyautoml"
__how_to__ = ["python -m unittest test.test_connector"]


import os
import gc
import atexit
import unittest
import tracemalloc
from utils import (
    run_makefile,
    absolute_path,
)
from email_connector import EmailConnector


class TestConnector(unittest.TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    atexit.register(run_makefile, "remove", path)

    def setUp(self) -> None:
        tracemalloc.start()
        self.connector = EmailConnector("pyautoml")
        self.connector_duplicate = EmailConnector("pyautoml")

    def tearDown(self) -> None:
        tracemalloc.stop()

    def test_positive_singleton_instance(self) -> None:
        """There should be always one class instance."""

        self.assertEqual(id(self.connector), id(self.connector_duplicate))
        self.assertTrue(self.connector, self.connector_duplicate)

    def test_positive_verify_forbidden_access(self) -> None:
        """Forbidden attributes should not be accessed via class instance."""

        for attribute in ["cat", "_load_settings"]:
            self.assertNotIn(attribute, [self.connector._forbidden_access])

    def test_positive_setting_blocked_attribute(self) -> None:
        """Setting new attribute should not be possible."""

        result = setattr(self.connector, "cat", "cat")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
    gc.collect()
1~#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

__created__ = "30.10.2023"
__last_uodate__ = "30.10.2023"
__author__ = "https://github.com/pyautoml"
__how_to__ = ["python -m unittest test.test_connector"]

import os
import gc
import atexit
import unittest
import tracemalloc
from utils import (
    run_makefile,
    absolute_path,
)
from email_connector import EmailConnector



class TestConnector(unittest.TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    atexit.register(run_makefile, "remove", path)

    def setUp(self) -> None:
        tracemalloc.start()
        self.connector = EmailConnector("pyautoml")
        self.connector_duplicate = EmailConnector("pyautoml")

    def tearDown(self) -> None:
        tracemalloc.stop()

    def test_positive_singleton_instance(self) -> None:
        """There should be always one class instance."""

        self.assertEqual(id(self.connector), id(self.connector_duplicate))
        self.assertTrue(self.connector, self.connector_duplicate)

    def test_positive_verify_forbidden_access(self) -> None:
        """Forbidden attributes should not be accessed via class instance."""

        for attribute in ["cat", "_load_settings"]:
            self.assertNotIn(attribute, [self.connector._forbidden_access])

    def test_positive_setting_blocked_attribute(self) -> None:
        """Setting new attribute should not be possible."""

        result = setattr(self.connector, "cat", "cat")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
    gc.collect()

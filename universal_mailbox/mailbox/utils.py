#!/usr/bin/python3.11
# -*- coding: utf-8 -*-

__created__ = "30.10.2023"
__last_udate__ = "02.11.2023"
__author__ = "https://github.com/pyautoml"
__how_to__ = ["python -m unittest test.test_utils"]


import gc
import os
import sys
import json
import atexit
import unittest
import tracemalloc
from utils import (
    run_makefile,
    absolute_path,
)


class TestUtils(unittest.TestCase):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    atexit.register(run_makefile, "remove", path)

    def setUp(self) -> None:
        tracemalloc.start()
        self.example_file = absolute_path("settings.json")
        self.expected_dict = {
            "user": "user",
            "password": "password",
        }

        with open(self.example_file, "w") as file:
            file.write(json.dumps(self.expected_dict))

    def tearDown(self) -> None:
        tracemalloc.stop()
        if os.path.exists(self.example_file):
            try:
                os.remove(self.example_file)
            except:
                pass


if __name__ == "__main__":
    unittest.main()
    gc.collect()

#!/usr/bin/python3.11

__created__ = "18.03.2023"
__last_update__ = ""
__author__ = "https://github.com/pyautoml"
__license__ = "https://github.com/pyautoml/automation/blob/main/License.txt"

"""
Regular expressions patterns for extracting data from Gmail messages.
"""


import re

patterns = {
    "gmail": {
        "email": re.compile(r"<(.*?)>"),
        "sender": re.compile(r"(?<=From: )([^<]+)"),
    },
    "security": {
        "arc_regex": re.compile(r"arc=([^;]*)"),
        "oda_regex": re.compile(r"oda=([^;]*)"),
    },
}

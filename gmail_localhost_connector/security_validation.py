#!/usr/bin/python3.11

__created__ = "18.03.2023"
__last_update__ = ""
__author__ = "https://github.com/pyautoml"
__license__ = "https://github.com/pyautoml/automation/blob/main/License.txt"


"""
Security support functions for data email validation.
"""


import re
import json
import email
from patterns import patterns
from email.header import decode_header
from dataclasses import dataclass, field


@dataclass
class GmailContentSecurity:
    oda_pattern: str = patterns["security"]["oda_regex"]
    arc_pattern: str = patterns["security"]["arc_regex"]

    def arc_seal_header(self, email_payload_headers: dict):
        """
        ARC-Seal header provides essential cryptographic information that helps in validating the email's authenticity,
        ensuring that the email has not been tampered with and originates from a legitimate source. This header is a
        critical component in email security protocols to prevent email spoofing and ensure the trustworthiness of email communications.

        Parameters explanation:
        > i=1: Indicates the cryptographic algorithm used for sealing the message, in this case, RSA with SHA-256.
        > t=1710699146: Represents the timestamp when the message was sealed, aiding in verifying the timeliness of the email.
        > cv=none: Denotes the cryptographic verification status, indicating that no verification failures were encountered.
        > d=google.com: Specifies the domain responsible for sealing the message, in this case, Google.
        > s=arc-20160816: Identifies the service that applied the ARC-Seal, which is the ARC (Authenticated Received Chain) protocol.
        > b=...: Contains the actual cryptographic seal that ensures the integrity and authenticity of the email content.
        """

        arc_auth_results = email_payload_headers.get("ARC-Authentication-Results", None)
        if arc_auth_results:
            arc_match = re.search(self.arc_pattern, arc_auth_results)
            oda_match = re.search(self.oda_pattern, arc_auth_results)

            if arc_match and oda_match:
                arc_found = arc_match.group()
                oda_found = oda_match.group()

                if arc_found == "pass" and oda_found == 1:
                    print("ARC verified successfully")
                else:
                    print("ARC verification failed")
            else:
                print("ARC or ODA not found in ARC-Authentication-Results header")
        else:
            print("ARC-Authentication-Results header not found")

    def handle_arc_seal(self, email_payload_headers: dict):
        arc_seal = email_payload_headers.get("ARC-Seal", None)

        if arc_seal:
            print("ARC-Seal:\n", arc_seal)
            arc_seal_parts = arc_seal.split(";")
            if len(arc_seal_parts) < 6:
                print("Invalid ARC-Seal")
                return
            print("i =", arc_seal_parts[0].strip().split("=")[1])
            print("a =", arc_seal_parts[1].strip().split("=")[1])
            print("t =", arc_seal_parts[2].strip().split("=")[1])
            print("cv =", arc_seal_parts[3].strip().split("=")[1])
            print("d =", arc_seal_parts[4].strip().split("=")[1])
            print("s =", arc_seal_parts[5].strip().split("=")[1])
            print("b =", arc_seal_parts[6].strip().split("=")[1])

    def handle_arc_seal(self, arc_seal: str):
        print("ARC-Seal:\n", arc_seal)
        arc_seal_parts = arc_seal.split(";")
        if len(arc_seal_parts) < 6:
            print("Invalid ARC-Seal")
            return
        print("i =", arc_seal_parts[0].strip().split("=")[1])
        print("a =", arc_seal_parts[1].strip().split("=")[1])
        print("t =", arc_seal_parts[2].strip().split("=")[1])
        print("cv =", arc_seal_parts[3].strip().split("=")[1])
        print("d =", arc_seal_parts[4].strip().split("=")[1])
        print("s =", arc_seal_parts[5].strip().split("=")[1])
        print("b =", arc_seal_parts[6].strip().split("=")[1])

    def handle_arc_authentication_results(self, arc_authentication_results: str):
        print("ARC-Authentication-Results:\n", arc_authentication_results)
        arc_auth_results_parts = arc_authentication_results.split(";")
        if len(arc_auth_results_parts) < 4:
            print("Invalid ARC-Authentication-Results")
            return
        print("i =", arc_auth_results_parts[0].strip().split("=")[1])
        print("mx.google.com =", arc_auth_results_parts[1].strip().split("=")[1])
        print("dkim =", arc_auth_results_parts[2].strip().split(" ")[1])
        print("spf =", arc_auth_results_parts[3].strip().split(" ")[1])

    def handle_arc_message_signature(self, arc_message_signature: str):
        print("ARC-Message-Signature:\n", arc_message_signature)
        signature_parts = arc_message_signature.split(";")
        if len(signature_parts) < 4:
            print("Invalid ARC-Message-Signature")
            return
        print("i =", signature_parts[0].strip().split("=")[1])
        print("a =", signature_parts[1].strip().split("=")[1])
        print("c =", signature_parts[2].strip().split("=")[1])
        print("d =", signature_parts[3].strip().split("=")[1])

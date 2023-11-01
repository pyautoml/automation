# Universal Private Email Connector

## A library that automates connections to popular email services such as Gmail, Outlook, AOL, Apple, Yahoo.
The library is used to support private accounts that have not been migrated to cloud services.
If you require additional library functions, please submit a request.

## Makefile
To successfully run Makefile (e.g. make remove) please use GitBash or any other Linux terminal.

## Tests

### Change settings before running tests

1) In files test_email_connector.py and test_email_parser.py change email settings to the one matching your configuration/settings.json file.

    Assuming that the settings.json file content is:
    {
        "adam": {
            "email_address": "example@outlook.com",
            "email_password": "password",
            "imap_port": 993
        }
        
    }

#### In test_email_connector.py:


    Change from:
        def setUp(self) -> None:
            tracemalloc.start()
            self.connector = EmailConnector("your_user", email_provider="email_provider")
            self.connector_duplicate = EmailConnector("your_user", email_provider="email_provider")

    To:
        def setUp(self) -> None:
            tracemalloc.start()
            self.connector = EmailConnector("example", email_provider="outlook")
            self.connector_duplicate = EmailConnector("your_user", email_provider="outlook")

#### In test_email_parser.py:

    Change from:

        def setUp(self) -> None:
            tracemalloc.start()
            self.connector = EmailConnector("your_user", email_provider="email_provider")

    To:
        def setUp(self) -> None:
            tracemalloc.start()
            self.connector = EmailConnector("example", email_provider="outlook")

2) To run tests, go to ~/mailbox/ and then: python -m unittest discover

## Description:
A file with examples of how to use the library will be added. 
At this point, perform the following plugins to start the service:
1) Download the files. In the **configuration** directory, write the **settings.py** file with the access data for your email account.
2) Create an object of class EmailConnector, such as:

user_account = EmailConnector("key_name_under_which_you_added_user_in_file_settings.json",console_messages=True)
user_account._connect()
user_account._disconnect()

Info: console_messages = True allows messages to be displayed in cmd. The default is set to False.
3) In mailbox/test change username in test_email_connector.py and test_email_parser.py to your own matching data in settings.py
Examples:
    self.connector = EmailConnector("your_user", email_provider="your_email_provider")

## TODO
This library is under development. The following steps will be supported:
1) reading and parsing attachments
2) extraction, cleaning and reading of preferred fields from the email (addressee, sender, subject, body, etc.).
3) handling the filtering of results
4) log handling

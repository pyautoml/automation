# Universal Private Email Connector

## A library that automates connections to popular email services such as Gmail, Outlook, AOL, Appe, Yahoo.
The library is used to support private accounts that have not been migrated to cloud services.
If you require additional library functions, please submit a request.

## Description:
A file with examples of how to use the library will be added. 
At this point, perform the following plugins to start the service:
1) Download the files. In the **configuration** directory, write the **settings.py** file with the access data for your email account.
2) Create an object of class EmailConnector, such as:

user_account = EmailConnector("key_name_under_which_you_added_user_in_file_settings.json",console_messages=True)
user_account._connect()
user_account._disconnect()

Info: console_messages = True allows messages to be displayed in cmd. The default is set to False.


## TODO
This library is under development. The following steps will be supported:
1) reading and parsing attachments
2) extraction, cleaning and reading of preferred fields from the email (addressee, sender, subject, body, etc.).
3) handling the filtering of results
4) log handling

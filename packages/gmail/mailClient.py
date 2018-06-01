# coding: utf8

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from os import path, environ

import smtplib


class MailClient():

    # Member variables
    SENDER_EMAIL = ''
    SENDER_PASSWORD = ''
    RECEIVER_EMAILS = []

    def __init__(self):
        self.loadAccountFromDotenv()

    def loadAccountFromDotenv(self):
        # Load my email addresses and password from ./.env
        load_dotenv(path.join(path.dirname(__file__), '../../.mailaccount'))
        self.SENDER_EMAIL = environ.get('SENDER_EMAIL')
        self.SENDER_PASSWORD = environ.get('SENDER_PASSWORD')
        self.RECEIVER_EMAILS = environ.get('RECEIVER_EMAILS').split(',')

    def _contains_non_ascii_characters(self, str):
        '''
        Helper function
        Check whether a string contains non-ascii characters
        '''
        return not all(ord(c) < 128 for c in str)

    def add_header(self, message, header_name, header_value):
        # Functions to generate email message string
        if self._contains_non_ascii_characters(header_value):
            h = Header(header_value, 'utf-8')
            message[header_name] = h
        else:
            message[header_name] = header_value
        return message

    def send(self, subject, content):
        # Send email to myself
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)

        # Generate email message string
        msg = MIMEMultipart('alternative')
        msg = self.add_header(msg, 'Subject', subject)
        if(self._contains_non_ascii_characters(content)):
            plain_text = MIMEText(content.encode('utf-8'),'plain','utf-8')
        else:
            plain_text = MIMEText(content,'plain')
        msg.attach(plain_text)

        smtpObj.sendmail(self.SENDER_EMAIL, self.RECEIVER_EMAILS, str(msg))
        smtpObj.quit()
        print('Email sent')

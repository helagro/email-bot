import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import credentials

imap = imaplib.IMAP4_SSL("imap.gmail.com")

def getAndParseEmails():
    status, messages = imap.select("INBOX")
    #(retcode, messages) = imap.search(None, '(UNSEEN)')
    n=0
    for num in messages[0].split() :
        n=n+1
        typ, data = imap.fetch(num,'(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                original = email.message_from_bytes(response_part[1])
                body = original.get_payload()

                print (original['From'])
                print (original['Subject'])
                print("eno", body[0])
                typ, data = imap.store(num,'+FLAGS','\\Seen')

def reloadMailbox():
    getAndParseEmails()

def setup():
    imap.login(credentials.username, credentials.password)


    




def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
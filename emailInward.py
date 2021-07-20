from email import message
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import credentials

imap = imaplib.IMAP4_SSL("imap.gmail.com")


def emailToMap(emailMessage):
    emailMap = {}


    if emailMessage.is_multipart():
        for payload in emailMessage.get_payload():
            print (payload.get_payload())
    else:
        print (emailMessage.get_payload())

    #emailMap["message"]
    emailMap["from"] = emailMessage['From']
    emailMap["subject"] = emailMessage['Subject']

    #print("clips", emailMap["message"].as_string())
    print("eno", emailMap)
    #typ, data = imap.store(num,'+FLAGS','\\Seen')
    return emailMap


def getEmailMessage(emailIndex):
    resCode, data = imap.fetch(emailIndex,'(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            return emailToMap(email.message_from_bytes(response_part[1]))





def getEmailMessages(emailAccessors):   
    messages = []

    for emailAccessorsGroup in emailAccessors:
        for emailIndex in emailAccessorsGroup.split() :
            message = getEmailMessage(emailIndex)
            messages.append(message)


def getNewEmails():
    inboxResCode, latestEmailAccessor = imap.select("INBOX")
    #return imap.search(None, '(UNSEEN)')
    return inboxResCode, latestEmailAccessor


def getAndParseEmails():
    resCode, newEmailAccessors = getNewEmails()
    getEmailMessages(newEmailAccessors)


def reloadMailbox():
    getAndParseEmails()

def setup():
    imap.login(credentials.username, credentials.password)


    




def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)
from email import message
import imaplib
import email
from email.header import decode_header
import credentials
import threading
import time

imap = imaplib.IMAP4_SSL("imap.gmail.com")
refreshDelay = 300
shouldListenForEmails = False


def stopListeningForEmails():
    global shouldListenForEmails
    shouldListenForEmails = False


def getEmailBodyString(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            try:
                body = part.get_payload(decode=True).decode()
            except:
                pass
            if content_type == "text/plain":
                return body
    else:
        content_type = msg.get_content_type()
        body = msg.get_payload(decode=True).decode()
        if content_type == "text/plain":
            return body
        if content_type == "text/html":
            pass

def getMessageItemAsString(name, msg):
    item, encoding = decode_header(msg[name])[0]
    if isinstance(item, bytes):
        return item.decode(encoding)
    return item

def emailToMap(msg):
    emailMap = {}

    emailMap["subject"] = getMessageItemAsString("Subject", msg)
    emailMap["from"] = getMessageItemAsString("From", msg)
    emailMap["body"] = getEmailBodyString(msg)

    return emailMap

def getEmailMessage(emailIndex):
    resCode, data = imap.fetch(emailIndex,'(RFC822)')
    for response_part in data:
        if isinstance(response_part, tuple):
            typ, data = imap.store(emailIndex,'+FLAGS','\\Seen')
            return emailToMap(email.message_from_bytes(response_part[1]))


def getEmailMessages(emailAccessors):   
    messages = []

    for emailAccessorsGroup in emailAccessors:
        for emailIndex in emailAccessorsGroup.split() :
            message = getEmailMessage(emailIndex)
            messages.append(message)

    return messages

def getNewEmails():
    inboxResCode, latestEmailAccessor = imap.select("INBOX")
    return imap.search(None, '(UNSEEN)')
    #return inboxResCode, latestEmailAccessor

def getAndParseEmails():
    resCode, newEmailAccessors = getNewEmails()
    return getEmailMessages(newEmailAccessors)

def reloadMailbox():
    messages = getAndParseEmails()
    print("inbox:", messages)


def listenForEmailsLoop():
    while shouldListenForEmails:
        reloadMailbox()
        time.sleep(refreshDelay)

def startListeningForEmails():
    global shouldListenForEmails
    shouldListenForEmails = True
    threading.Thread(target=listenForEmailsLoop, group=None).start()


def setup():
    imap.login(credentials.username, credentials.password)

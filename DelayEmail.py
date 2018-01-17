import smtplib
import getpass
import sys
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email

#Notes: Gmail account must have "allow less secure apps" settings turned on to work

# created with help from https://medium.com/@williamr/how-to-send-an-email-from-a-gmail-account-with-python-b5b6e44c27b6
    # and http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
    # and http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/

def getUser():
    print("\nLogging in to Gmail (Gmail's allow less secure apps settings must be on)\n")
    return input("Enter Username:")
def getPass():
    return getpass.getpass("Enter Password:")
def getRecipent():
    return input("Enter recipient address:")
def getSubject():
    return input("Enter Email Subject:")
def getBodyfromInput():
    print("Enter Email Body(Use -1 on a separate line to save):\n")
    body = ""
    while True:
        line=input()
        if line == "-1":
            break
        body = body + line + "\n"

        '''
        try:
            line = input()
        except EOFError:
            break
        body = body + line + "\n"
        '''
    body = body[:-1] #remove last newLine
    return body

# LIMITATIONS: does not work after createEmail is called bc of MIMETEXT to str conversion?? IDK
def getBodyfromEmail(email):
    body = ""
    if email.is_multipart():
        for payload in email.get_payload()[:-1]:
           body += payload.get_payload()
    else:
        body = email.get_payload()
    body = body[:-1]  # extra newline for some reason
    return body
def imapSetup(username, password): # connect to GMAIL server through imap # remember to logout
    imapObj = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        imapObj.login(username, password)
    except imaplib.IMAP4.error:
        print("Incorrect Login")
        sys.exit()
    return imapObj

def smtpSetup(username,password): # connect to GMAIL server through smtp # remember to logout
    session = smtplib.SMTP('smtp.gmail.com',587) #connect to gmail server
    session.ehlo() # initiate connection to server
    session.starttls() # encrypt messages to server
    session.login(username, password)
    print("Login successful\n")
    return session


# does not accommodate CC or BCC header values
#does not verify validity of sender,recipient email addresses
# does not support attachments
def createEmail(sender,recipient,subject,body):
    # create  headers
    email = MIMEMultipart()
    email['From'] = sender
    email['To'] = recipient
    email['Subject'] = subject
    email.attach(MIMEText(body[:-1],'plain')) #body[:-1] gets rid of extra newLine
    print("Email Created successfully\n")
    return email

# takes smtp object
def sendEmail(sender, session, message): #takes sender, smtp object, email object
    print("Creating email\n")
    recipient = message['To']
    email = message.as_string()
    session.sendmail(sender,recipient,email)
    print("Email Sent\n")

def printEmail(email): #takes email object
    print(email['From'])
    print(email['To'])
    print(email['Subject'])
    print(getBodyfromEmail(email))

# returns ID of email with the specified search criteria(recipient, subject) in the specified mailbox
    # if multiple emails match the search criteria, the ID of the first one will be returned (not sure if first=most recent or opposite)
def getEmailID(imapObj, mailbox, searchRecipient, searchSubject):
    status, Mailbox = imapObj.select(mailbox)
    if status == 'OK':
        status, searchResult = imapObj.search(None, 'TO', searchRecipient, 'SUBJECT', searchSubject)
        if status == 'OK':
            IDList = searchResult[0].split()  # returns a list of email ids that have the match
            ID = IDList[0]
            return ID
        else:
            print("search not okay")
    else:
        print("select not okay")

#returns email ID and email contents (sender,recipient,subject,body) from Drafts
def retrieveDrafts(imapObj):
    print("Retrieving Drafts (Make sure there is only one email with same subject and recipient)")
    mailbox = "[Gmail]/Drafts"
    recipient = getRecipent()
    subject = getSubject()
    ID = getEmailID(imapObj,mailbox,recipient,subject)

    status, fetchResult = imapObj.fetch(ID, '(RFC822)')
    if status == 'OK':
        message = email.message_from_bytes(fetchResult[0][1])
        retTuple = (ID,message)
        return retTuple
    else:
        print("fetch not okay")

def deleteEmail(imapObj,emailID, mailbox):
    imapObj.store(emailID, '+FLAGS', '\\Deleted')
    imapObj.expunge()

def sendFromDrafts(session, imapObj): #recieves smtp object and imap object
    draftTuple = retrieveDrafts(imapObj)
    draftID = draftTuple[0]
    draftMessage = draftTuple[1]
    sender = draftMessage['From']
    recipient = draftMessage['To']
    subject = draftMessage['Subject']
    body = getBodyfromEmail(draftMessage)
    email = createEmail(sender,recipient,subject,body) # creates temp email for sending through smtp
    sendEmail(sender, session, email)
    mailbox = "[Gmail]/Drafts"
    deleteEmail(imapObj,draftID, mailbox)

def main():
    username = getUser()
    password = getPass()
    imapObj = imapSetup(username, password)
    session = smtpSetup(username, password)
    sendFromDrafts(session,imapObj)
    session.quit() #close connection to smtp server
    imapObj.logout()

if __name__ == '__main__':
    main()
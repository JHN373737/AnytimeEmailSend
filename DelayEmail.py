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
def getBody():
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

def imapSetup(username, password): # connect to GMAIL server through imap
    imapObj = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        imapObj.login(username, password)
    except imaplib.IMAP4.error:
        print("Incorrect Login")
        sys.exit()
    return imapObj

def smtpSetup(username,password): # connect to GMAIL server through smtp
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
    email.attach(MIMEText(body,'plain'))
    print("Email Created successfully\n")
    return email

# takes smtp object
def sendEmail(session):
    print("Creating email\n")
    recipient = getRecipent()
    email = createEmail(username,recipient,getSubject(),getBody())
    email = email.as_string()
    session.sendmail(username,recipient,email)
    print("Email Sent\n")
    #close connection to smtp server
    session.quit()

def retrieveDrafts(imapObj):
    #imap functions typically return tuple with 1st element = return status, 2nd element = data
    print("Retrieving Drafts (Make sure there is only one email with same subject and recipient)")
    status, draftsMailbox = imapObj.select("[Gmail]/Drafts")
    ########################### seperate into getMailbox, getEmail ##################
    if status=='OK':
        recipient = getRecipent()
        subject = getSubject()
        status, draftsSearch = imapObj.search(None,'TO',recipient,'SUBJECT',subject)
        if status=='OK':
            draftIDList = draftsSearch[0].split() # returns a list of email ids that have the match
            draftID = draftIDList[0]
            print(draftID)
            status, draftFetch = imapObj.fetch(draftID,'(RFC822)')
            print(draftFetch[0][1])
            if status == 'OK':
                draftMessage = email.message_from_string(draftFetch[0][1])
                print('Message: %s' % (draftMessage['Subject']))

                #print(draftMessage['Subject'])
                #print(draftMessage['To'])
            else:
                print("fetch not okay")
        else:
            print("search not okay")

    else:
        print("select not okay")

def main():
    username = getUser()
    password = getPass()
    imapObj = imapSetup(username, password)
    #session = smtpSetup(username, password)
    #session.quit()
    retrieveDrafts(imapObj)
    imapObj.logout()


if __name__ == '__main__':
    main()
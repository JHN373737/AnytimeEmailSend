import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Notes: Gmail account must have "allow less secure apps" settings turned on to work

# created with help from https://medium.com/@williamr/how-to-send-an-email-from-a-gmail-account-with-python-b5b6e44c27b6
    # and http://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email/
    # and

def getUser():
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

def smtpSetup():
    session = smtplib.SMTP('smtp.gmail.com',587) #connect to gmail server
    session.ehlo() # initiate connection to server
    session.starttls() # encrypt messages to server
    print("Logging in to Gmail\n")
    session.login(getUser(),getPass())
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

def sendEmail():
    session = smtpSetup()

    print("Creating email\n")
    user = getUser()
    recipient = getRecipent()
    email = createEmail(user,recipient,getSubject(),getBody())
    email = email.as_string()
    session.sendmail(user,recipient,email)
    print("Email Sent\n")
    #close connection to smtp server
    session.quit()

def main():
    sendEmail()
if __name__ == '__main__':
    main()
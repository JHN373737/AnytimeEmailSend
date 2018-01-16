import requests
import quickstart

def getProfile():
    GMAIL = quickstart.get_service()
    #threads = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
    profile = GMAIL.users().getProfile(userId='willwilliams752@gmail.com').execute()
    print(profile)
    '''
    threads1 = GMAIL.users().threads().list(userId='me').execute().get('threads', [])
    print(threads1)
    print('\n') 
    threads = GMAIL.users().threads().list(userId='me')
    print(threads)
    '''

if __name__ == '__main__':
    getProfile()
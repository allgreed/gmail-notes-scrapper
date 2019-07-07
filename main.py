import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['Label_2']).execute()

    m = results['messages']

    latest, cutoff = None, None
    with open('cutoff') as f:
        ghh = f.readlines()
        try:
            cutoff = ghh[0].rstrip()
        except IndexError:
            pass

    for i, a in enumerate(m):
        if i == 0:
            latest = a['id']
            
        if a['id'] == cutoff:
            break

        r = service.users().messages().get(userId="me", id=a['id']).execute()
        import base64
        content = r['payload']['body']['data'] 
        ble = base64.urlsafe_b64decode(content.encode('ascii')).decode('utf-8')

        import re
        fuj = re.sub(r'<.*?>', '', ble)
        argh = fuj.rstrip()

        print(argh)

    #print("New cutoff %s" % latest)
    with open('cutoff', 'w') as f:
        f.write(latest)
        f.write('\n')

# TODO: Transfer to a propper project on desktop
# TODO: Put under git
# TODO: refactor
# TODO: Update cutoff point with journaling after going through the whole list
# TODO: Refactor as a module
# TODO: Save processed notes
# TODO: Document usage - how to obtain secrets, etc.
# TODO: Post on Github

if __name__ == '__main__':
    main()

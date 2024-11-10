import pickle
import os

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DEFAULT_NOTES_WHEN_MISSING_CUTOFF = 30


def main():
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
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            except FileNotFoundError:
                print("Go to https://developers.google.com/gmail/api/quickstart/python and generate credentials.json")
                exit(1)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', labelIds=['Label_2']).execute()

    m = results['messages']

    latest, cutoff = None, None
    try:
        with open('cutoff') as f:
            ghh = f.readlines()
        cutoff = ghh[0].rstrip()
    except (IndexError, FileNotFoundError):
            pass

    for i, a in enumerate(m):
        if i == 0:
            latest = a['id']
            
        if a['id'] == cutoff:
            break

        # handle missing cutoff
        if i == DEFAULT_NOTES_WHEN_MISSING_CUTOFF and cutoff is None:
            break

        r = service.users().messages().get(userId="me", id=a['id']).execute()
        import base64
        content = r["payload"]["body"]["data"] 
        ble = base64.urlsafe_b64decode(content.encode('ascii')).decode('utf-8')

        import html
        def parse_note_body(note_body) -> str:
            # '&lt;' -> '<'
            return html.unescape(note_body)

            # there's inner div
            # there's br
            
            # import re
            # fuj = re.sub(r'<.*?>', '', note_body)
            # argh = fuj.rstrip()
            # return argh

        # TODO: I only need to translant this actually
        # also: refactoring ble -> content would be nice, but one thing at a time
        print(parse_note_body(ble))
        exit(0)


if __name__ == '__main__':
    main()

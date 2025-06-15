import pickle
import os
import html
import html.parser

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
DEFAULT_NOTES_WHEN_MISSING_CUTOFF = 30

DEBUG = False


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
            print("ragadżaga!!!!!")
            break

        r = service.users().messages().get(userId="me", id=a['id']).execute()
        import base64
        content = r["payload"]["body"]["data"] 
        ble = base64.urlsafe_b64decode(content.encode('ascii')).decode('utf-8')

        print(parse_note_body(ble))
        if DEBUG:
            print("orig", ble)
    print("+1")
    print('cd ~/Desktop/ogar-metric-exporter; nix-shell --command "make report"')
    # TODO: actually just run the systemd service?

    if not DEBUG:
        with open('cutoff', 'w') as f:
            f.write("{}\n".format(latest))
        if cutoff != latest:  # prevents losing a backup
            with open('cutoff.bak', 'w') as f:
                f.write("{}\n".format(cutoff))

# TODO: unfuck
# TODO: Refactor as a module

# TODO: Update cutoff point with journaling after going through the whole list
# TODO: Don't 'move' to next note util the output is flushed to stdout

# TODO: Document usage - how to obtain secrets, etc. <- is this needed?


def parse_note_body(note_body) -> str:
    # print(note_body)
    arr = []
    class MyHTMLParser(html.parser.HTMLParser):
        def __init__(self, *args, **kwargs):
            self.ble = False
            self.newline = False
            super().__init__(*args, **kwargs)

        def handle_starttag(self, tag, _):
            # the br tags are often not closed, nor self-closed
            if tag in {"div", "br"}:
                self.ble = True
                self.newline = True
            elif tag in {"a", "body", "span"}:
                self.ble = True
                self.newline = False
            else:
                self.ble = False
                self.newline = False

        def handle_data(self, data):
            if self.ble:
                arr.append(data.replace("\r\n", "").replace("\xa0", " "))
            if self.newline:
                arr.append("\n")

    parser = MyHTMLParser()
    parser.feed(note_body)

    kek = list(filter(len, arr))
    return "".join(kek) + ("\n" if len(kek) > 1 and "\n" in kek else "")


if __name__ == '__main__':
    main()

import datetime
import pickle
import os.path
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = os.getcwd()+'/secret_json.json'


def get_calendar_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    
    with open(os.getcwd()+'/TempData/temp.txt', 'r') as username_file:
        username = username_file.read()
    
    if os.path.exists(f'{os.getcwd()}/{username}.pickle'):
        with open(f'{os.getcwd()}/{username}.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        # with open('token.pickle', 'wb') as token:
        #     pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0, mins=0):
    # made a few tweaks to the code:
    # - adjusts the time accordingly
    dt = (datetime.datetime(year, month, day, hour, minute, 0) +
          timedelta(minutes=mins)).isoformat() + 'Z'
    return dt

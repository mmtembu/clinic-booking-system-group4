from __future__ import print_function
import datetime
import time
import pickle
import os.path
import sys
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile,  get_user_info

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


# def login():
#     get_credentials('./credentials.json')
   

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    #Gets credentials for the user
    service = build('calendar', 'v3', credentials=get_credentials('./credentials.json'))

    #calls api service for the student's calendar
    events = call_api(service)

    #shows all events in the calendar
    view_calendar_events(events)


def view_calendar_events(events):
    #This has to be view calendar
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def call_api(service):
    # Call the Calendar API
    now = time.strftime(r'%Y-%m-%dT%H:%M:%SZ')
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary',timeZone='Africa/Johannesburg', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


def get_credentials(secret_json):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    username = ''
    does_existed,profile = get_user_info()
    print("show me what is happening?",does_existed, profile)
    if does_existed:
        username = profile["username"]
    else:
        return None

    creds = None

    if os.path.exists(f'{username}.pickle'):
        with open(f'{username}.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                secret_json, SCOPES)
            creds = flow.run_local_server(port=0)

            session = requests.sessions.Session()
            session['username']  = 'mmtembu'

        # Save the credentials for the next run
        with open(f'{username}.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return creds


def do_help():
    """Lists all the available commands"""
    print("""
  HELP       -   lists all the available commands the booking system provides
  BOOKING    -   allows a student to make a booking to an available slot
  CLINICIANS -   allows the student to view all the available clinicians
  CLINIX     -   shows coding clinix calendar events
  START      -   it starts the clinix appointment
  LOGOUT     -   use this command to remove your credentials from current system
          """)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == 'HELP':
            do_help()
        elif sys.argv[1].upper() == 'INIT':
            create_profile()
        elif sys.argv[1].upper() == 'LOGIN':
            main()            
    elif len(sys.argv) == 1:
        do_help()

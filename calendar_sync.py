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
from interface import get_user_info


SCOPES = ['https://www.googleapis.com/auth/calendar']


def view_calendar_events(events):
    #This has to be view calendar
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def call_api(calId,service):
    # Call the Calendar API
    now = time.strftime(r'%Y-%m-%dT%H:%M:%SZ')
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calId,timeZone='Africa/Johannesburg', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


def get_credentials(secret_json):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    username = ''
    does_existed,profile = get_user_info()
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

        # Save the credentials for the next run
        with open(f'{username}.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    return creds


def get_calendars():
    """
    This funtion gets both the calendars
    """
    secret_json = './credentials.json'
    clinix =  'c_hhfm5kgrq1708jemoqc73941pg@group.calendar.google.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials('./credentials.json'))
    view_calendar_events(call_api(clinix, service))
    view_calendar_events(call_api(user_calendar, service))

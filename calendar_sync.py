from __future__ import print_function
import datetime
import time
import pickle
import os.path
import sys
import requests
import csv
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile,  get_user_info


SCOPES = ['https://www.googleapis.com/auth/calendar']


def fetch_calendar_events(events, agent):
    # This has to be view calendar
    # if not events:
    #     print(f'No upcoming events found for {agent}.')
    # else:
        # print('DATE          |    TIME        |    DESCRIPTION')
        # print('________________________________________________')
    with open(f'{agent}.csv', 'w') as calendar:
        line = csv.writer(calendar, delimiter='\t',
                        quoting=csv.QUOTE_NONE, escapechar='\t')
        line.writerow(['DATE', '\tTIME', '\t\tDESCRIPTION'])
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['start'].get('date'))
            date = start.split('T')[0]
            time = f"{start.split('T')[1].split('+')[0]} - {end.split('T')[1].split('+')[0]}"


            # print(date, "   |   ", time, "   |   ", event['summary'])
            line.writerow([date+"   ", time+"   ", event['summary']])


def read_data(agent):
    if os.path.exists(f'{agent}.csv'):
        list = []
        with open(f'{agent}.csv', 'r') as file:
            csv_reader = (csv.DictReader(file))

            list = \
            [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
            .split('\t')[0].strip(),
            "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
            .split('\t')[1].strip(),
            "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
            .split('\t')[2].strip()} for row in csv_reader]
            
            if len(list) != 0:
                print(f'Getting the upcoming for the next 7 day [{agent}]\n')
                print('DATE          |            TIME           |    DESCRIPTION')
                print('_____________________________________________________________')
                
                [print(item['Date'], "   |   ", item['Time'],"   |   ", item['Description'])for item in list]
            else:
                print(f'No upcoming events found for {agent}.')
    else:
        print('User not logged in')

def call_api(service, cID, agent):

    # Call the Calendar API
    now = time.strftime(r'%Y-%m-%dT%H:%M:%SZ')
    day = int(datetime.today().strftime('%d')) + 7
    month = datetime.today().strftime('%m')
    year = datetime.today().strftime('%Y')
    hour = datetime.today().strftime('%H')
    minutes = datetime.today().strftime('%M')
    secs = datetime.today().strftime('%SZ')
    end = f"{year}-{month}-{day}T{hour}:{minutes}:{secs}"
    events_result = service.events().list(calendarId=cID, timeZone='Africa/Johannesburg', timeMin=now, timeMax = end,singleEvents=True,orderBy='startTime').execute()
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
    # clinix =  'c_hhfm5kgrq1708jemoqc73941pg@group.calendar.google.com'
    clinix =  'codeclinix@gmail.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials(secret_json))
    fetch_calendar_events(call_api(service, clinix, 'clinix'), 'clinix')
    fetch_calendar_events(call_api(service ,user_calendar, 'student'), 'student')
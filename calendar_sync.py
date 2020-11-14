from __future__ import print_function
import datetime
import time
import pickle
import os.path
import sys
import requests
import csv
import hashlib
import uuid
import difflib
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile,  get_user_info


SCOPES = ['https://www.googleapis.com/auth/calendar']


def fetch_calendar_events(events, agent):
    """
        This function gets data from the api and writes the data to a csv file

    Args:
        events ([list]): events returned by the api
        agent ([string]): this is either the student or the clinix
    """

    if is_calendar_current_data_old(events, agent) == "no data" or not is_calendar_current_data_old(events, agent):
        with open(f'{agent}.csv', 'w') as calendar:
            line = csv.writer(calendar, delimiter='\t',
                              quoting=csv.QUOTE_NONE, escapechar='\t')
            line.writerow(['DATE', '\tTIME', '\t\tDESCRIPTION'])
            for event in events:
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['start'].get('date'))
                date = start.split('T')[0]
                time = f"{start.split('T')[1].split('+')[0]} - {end.split('T')[1].split('+')[0]}"
                line.writerow([date+"   ", time+"   ", event['summary']])
    else:
        print(f'No updates were made to the {agent} calendar.')


def is_calendar_current_data_old(events, agent):
    """ This file checks whether data the user has is latest

    Args:
        events ([list]): events returned by the api
        agent ([string]): this is either the student or the clinix
    """

    if os.path.exists(f'{agent}.csv'):
        file_in_system = from_csv_to_dict(agent)
        data_from_api = [{
            "Date": event['start'].get('dateTime', event['start'].get('date')).split('T')[0],
            "Time":f"{event['start'].get('dateTime', event['start'].get('date')).split('T')[1].split('+')[0]} - {event['end'].get('dateTime', event['start'].get('date')).split('T')[1].split('+')[0]}",
            "Description":event['summary']}
            for event in events]

        # returns true if there's a difference in the data
        # return false if there there's no difference in the data
        return list(difflib.unified_diff(
            str(file_in_system), str(data_from_api))) == []
        # returns a string no data if the csv file doesn't exist
    return 'no data'


def from_csv_to_dict(agent):
    """
    This function converts contents from the csv file to a list
    """
    list = []
    with open(f'{agent}.csv', 'r') as file:
        csv_reader = (csv.DictReader(file))
        list = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                 .split('\t')[0].strip(),
                 "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                 .split('\t')[1].strip(),
                 "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                 .split('\t')[2].strip()} for row in csv_reader]
    return list


def read_data(agent):
    if os.path.exists(f'{agent}.csv'):
        if len(from_csv_to_dict(agent)) != 0:
            print(f'Getting the upcoming for the next 7 days [{agent}]\n')
            print('DATE          |            TIME           |    DESCRIPTION')
            print('_____________________________________________________________')

            [print(item['Date'], "   |   ", item['Time'],
                   "   |   ", item['Description'])for item in from_csv_to_dict(agent)]
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
    events_result = service.events().list(calendarId=cID, timeZone='Africa/Johannesburg',
                                          timeMin=now, timeMax=end, singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])


def get_credentials(secret_json):
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    username = ''
    does_existed, profile = get_user_info()
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

    # secret_json = os.getcwd()+'/.config/clinix/credentials.json'
    secret_json = 'credentials.json'
    # clinix =  'c_hhfm5kgrq1708jemoqc73941pg@group.calendar.google.com'
    clinix = 'codeclinix@gmail.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials(secret_json))
    fetch_calendar_events(call_api(service, clinix, 'clinix'), 'clinix')
    fetch_calendar_events(
        call_api(service, user_calendar, 'student'), 'student')

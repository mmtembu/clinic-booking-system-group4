from __future__ import print_function
import datetime
from datetime import timedelta
import time
import pickle
import prettytable
import os.path
import sys
import requests
import csv
import hashlib
import uuid
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile,  get_user_info
from make_booking.make_booking2 import create_booking


SCOPES = ['https://www.googleapis.com/auth/calendar']
username = ""


def fetch_calendar_events(events, agent):
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
        print(f'Getting the upcoming for the next 7 days [{agent}]\n')
        base_day = datetime.today()
        date_list = [(base_day + timedelta(days=x, minutes=60)).strftime(r'%Y %d %BD%A')
                     # (r'%Y-%b-%d %a')(r'%Y-%b-%d %a')(r'%Y-%B-%d %A')(r'%Y %d %BD%A')(r'%Y-%m-%d')

                     for x in range(7)]
        # print(date_list)

        dates_ = [item['Date'] for item in from_csv_to_dict(agent)]

        times_ = [item['Time'].split('-')[0].strip()
                  for item in from_csv_to_dict(agent)]

        base_time = datetime(int(datetime.today().strftime("%Y")), int(datetime.today().strftime("%m")), int(
            datetime.today().strftime("%d")), 8, 30)

        time_list = [(base_time + timedelta(minutes=x)).strftime(r'%H:%M:%S')
                     for x in range(0, 481, 30)]

        ptable = prettytable.PrettyTable()
        ptable.add_column('Time', time_list)

        table = []
        for x in range(7):
            base_day = datetime.today()
            date_from_user = (base_day + timedelta(days=x, minutes=60)
                              ).strftime(r'%Y-%m-%d')
            table_slot = view_all_slots(date_from_user,
                                        from_csv_to_dict(agent))
            col = []
            for item in table_slot:
                # ptable.add_row(
                #     [item['Date'], item['Time'], item['Description'], ])
                # ptable.add_row(
                col.append(item['Description'])
                # ptable.add_row(
                #     [item['Date'], item['Time'], item['Description']])
            date = item['Date']
            date = datetime.strptime(date, '%Y-%m-%d').date()
            # print(date.strftime('%Y-%B-%A'))
            date = date.strftime("%Y-%B-%A-%d")
            day = str(date).split('-')[2]
            day_date = str(date).split('-')[3]
            day_year = str(date).split('-')[0]
            ptable.add_column(
                f"{day_date} {str(date).split('-')[2]} {day_year}", col)
        print(ptable)


def view_all_slots(day, list_of_slots):

    list_of_times = []
    base_time = datetime(int(datetime.today().strftime("%Y")), int(
        datetime.today().strftime("%m")), int(datetime.today().strftime("%d")), 8, 30)

    list_of_times = [{"Date": day, "Time": (base_time + timedelta(minutes=x)).strftime(
        r'%H:%M:%S'), "Description": "----"} for x in range(0, 481, 30)]

    slots = []
    # print(list_of_slots)
    for item in list_of_slots:
        if day == item['Date']:
            slots.append(
                {"Date": item['Date'],
                 "Time": item['Time'].split('-')[0].strip(),
                 "Description": item['Description']})

    for i in slots:
        for j in list_of_times:
            if i["Time"].split('-')[0].strip() == j['Time'] and i["Date"] == j['Date']:
                list_of_times.insert(list_of_times.index(
                    j), {"Date": i['Date'], "Time": i['Time'].split('-')[0].strip(), "Description": i['Description']})
                list_of_times.pop(list_of_times.index(j))
    return list_of_times


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
    global username
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
    secret_json = os.getcwd()+'/credentials.json'
    # clinix =  'c_hhfm5kgrq1708jemoqc73941pg@group.calendar.google.com'
    clinix = 'codeclinix@gmail.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials(secret_json))
    fetch_calendar_events(call_api(service, clinix, 'clinix'), 'clinix')
    fetch_calendar_events(
        call_api(service, user_calendar, 'student'), 'student')


def volunteer_slot(agent):
    if os.path.exists(f'{agent}.csv'):
        with open(f'{agent}.csv', 'r') as events_list:
            create_booking(username)
    else:
        print('User not logged in')


def book_slot():
    pass


def create_combined_csv(student_events, clinix_events):
    if os.path.exists(f'{student_events}.csv'):
        list_of_slots = []
        with open(f'{student_events}.csv', 'r') as file:
            student_csv_reader = (csv.DictReader(file))

            list_of_slots =\
                [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                  .split('\t')[0].strip(),
                  "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                  .split('\t')[1].strip(),
                  "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                  .split('\t')[2].strip()} for row in student_csv_reader]
            # print("list of lists for student", list_of_slots)

        with open(f'{clinix_events}.csv', 'r') as file:
            clinix_csv_reader = (csv.DictReader(file))

            list_of_slots_clinix = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                                     .split('\t')[0].strip(),
                                     "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                                     .split('\t')[1].strip(),
                                     "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                                     .split('\t')[2].strip()} for row in clinix_csv_reader]
            # print("list of lists for clinix", list_of_slots)

        # print(list_of_slots)
        # list_of_slots.append(list_of_slots)
        # result =  [{x['Date'], x['Time'], x['Description']} for x in list_of_slots + list_of_slots}].values()
        result2 = [x for x in list_of_slots + list_of_slots_clinix]

        result = sorted(result2, key=lambda i: (i['Date'], i['Time']))

        # print(result)
        # result = {x['id']:x for x in lst1 + lst2}.values()
        with open('combined_calendar_list.csv', 'w') as calendar:
            line = csv.writer(calendar, delimiter='\t',
                              quoting=csv.QUOTE_NONE, escapechar='\t')
            line.writerow(['DATE', '\tTIME', '\t\tDESCRIPTION'])
            for item in result:
                line.writerow(
                    [item['Date']+"   ", item['Time']+"   ", item['Description']])


'''def get_username():
    return username'''


'''def get_both_calendars():
     # secret_json = os.getcwd()+'/.config/clinix/credentials.json'
    secret_json = os.getcwd()+'/credentials.json'
    # clinix =  'c_hhfm5kgrq1708jemoqc73941pg@group.calendar.google.com'
    clinix = 'codeclinix@gmail.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials(secret_json))

    
        
    return call_api(service, clinix, 'clinix')'''

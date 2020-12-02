from __future__ import print_function
from datetime import timedelta, datetime
import re
import time
import pickle
import prettytable
import os.path
import sys
import requests
import csv
import hashlib
import uuid
import difflib
import textwrap
from collections import defaultdict
from slot_package import filter_slots
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile,  get_user_info
from create_volunteer.create_volunteer_slot import create_volunteer
from make_booking.make_booking import create_booking


SCOPES = ['https://www.googleapis.com/auth/calendar']
# Color
RED = "\033[1;31m%s\033"  # RED
GREEN = "\033[1;32m%s\033"  # GREEN
YELLOW = "\033[1;33m%s\033"  # Yellow
BLUE = "\033[1;34m%s\033"  # Blue
NEUTRAL = "\033[0m"  # Reset
username = ""
col = defaultdict(list)


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
            if agent == 'clinix':
                line.writerow(
                    ['DATE', '\tTIME', '\t\tID', '\t\t\tDESCRIPTION'])
            else:
                line.writerow(['DATE', '\tTIME', '\t\tDESCRIPTION'])
            for event in events:
                start = event['start'].get(
                    'dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['start'].get('date'))
                date = start.split('T')[0]
                time = f"{start.split('T')[1].split('+')[0]} - {end.split('T')[1].split('+')[0]}"
                if agent == 'clinix':
                    line.writerow(
                        [date+"   ", time+"   ", event['id'], "   ", event['summary']])
                else:
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

        if agent == "student":
            list = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                     .split('\t')[0].strip(),
                     "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                     .split('\t')[1].strip(),
                     "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                     .split('\t')[2].strip()} for row in csv_reader]
        elif agent == "clinix":
            list = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION']
                     .split('\t')[0].strip(),
                     "Time": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION']
                     .split('\t')[1].strip(),
                     "ID": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION']
                     .split('\t')[2].strip(),
                     "Description": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION']
                     .split('\t')[4].strip()} for row in csv_reader]
    return list


def create_col_dict():

    col = defaultdict(list)
    col[1, '08:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # one
    col[1, '09:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[1, '09:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[2, '10:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # two
    col[2, '10:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[2, '11:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[3, '11:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # three
    col[3, '12:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[3, '12:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[4, '13:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # four
    col[4, '13:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[4, '14:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[5, '14:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # five
    col[5, '15:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[5, '15:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[6, '16:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')  # six
    col[6, '16:30:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    col[6, '17:00:00'] = ("\033[1;34m%s\033[0m" % '---------').center(40, '-')
    return col


def col_change_to_available(col):

    for _id__, time in col:
        col[_id__, time] = ("\033[1;34m%s\033[0m" % '---------').center(26, '-')


def col_dict_set(col, id, key, set):
    col[id, key] = set


def col_dict_get_all(col):
    return col


def col_dict_get(id, key):
    return col[id, key]


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
                     for x in range(0, 511, 30)]

        # ptable = prettytable.PrettyTable()
        # ptable.add_column('Time', time_list)

        table = []
        for x in range(7):
            base_day = datetime.today()
            date_from_user = (base_day + timedelta(days=x, minutes=60)
                              ).strftime(r'%Y-%m-%d')
            table_slot = view_all_slots(date_from_user,
                                        from_csv_to_dict(agent))

            col = create_col_dict()
            col_status = create_col_dict()
            col_change_to_available(col_status)

            for item in table_slot:
                ptable = prettytable.PrettyTable()
                ptable.add_column('Time', time_list)
                if len(item['Time'].split('-')) == 2:
                    time_diff = str(datetime.strptime(
                        item['Time'].split('-')[1].strip(), '%H:%M:%S') - datetime.strptime(
                        item['Time'].split('-')[0].strip(), '%H:%M:%S'))
                    minutes = int(time_diff.split(':')
                                  [0]) * 60 + int(time_diff.split(':')[1])
                    first = datetime.strptime((item['Date'] + ' ' +
                                               item['Time'].split('-')[0].strip()), r'%Y-%m-%d %H:%M:%S')
                    last = datetime.strptime((item['Date'] + ' ' +
                                              item['Time'].split('-')[1].strip()), r'%Y-%m-%d %H:%M:%S')

                    if minutes == 30:
                        there_is_time = False
                        if agent == 'clinix':
                            block_id = 0
                            for _id_, time in col:
                                if time == str(first).split()[1].strip():
                                    there_is_time = True
                                    block_id = _id_

                            if there_is_time:
                                for _id_, time in col:
                                    if time == str(first).split()[1].strip():
                                        if block_id == _id_:
                                            col_dict_set(
                                                col_status, _id_,  time, 'AVAILABLE')

                            for _id_, time in col:
                                if block_id == _id_:
                                    item['Description'] = "\033[1;32m%s\033[0m" % item['Description']
                                    col_dict_set(col,
                                                 _id_, time, item['Description'])

                        elif agent == 'student' and 'Clinix' not in item['Description']:
                            while first < last:
                                for _id_, time in col:
                                    if time == str(first).split()[1].strip():
                                        item['Description'] = "\033[1;32m%s\033[0m" % item['Description']
                                        col_dict_set(col,
                                                     _id_, time, item['Description'])
                                first += timedelta(hours=0,
                                                   minutes=30, seconds=0)
                    else:
                        if agent == 'student':
                            while first < last:
                                for _id_, time in col:
                                    if time == str(first).split()[1].strip():
                                        item['Description'] = "\033[1;32m%s\033[0m" % item['Description']
                                        col_dict_set(col,
                                                     _id_, time, item['Description'])
                                first += timedelta(hours=0,
                                                   minutes=30, seconds=0)
            date = item['Date']
            date = datetime.strptime(date, '%Y-%m-%d').date()
            date = date.strftime("%Y-%B-%A-%d")
            day = str(date).split('-')[2]
            day_date = str(date).split('-')[3]
            day_year = str(date).split('-')[0]
            ptable.add_column(
                f"{day_date} {str(date).split('-')[2]} {day_year}", [*col_dict_get_all(col).values()])
            if agent == "clinix":
                ptable.add_column(
                    f"STATUS", [*col_dict_get_all(col_status).values()])
            ptable.align[f"{day_date} {str(date).split('-')[2]} {day_year}"] = 'l'
            print(ptable)
    else:
        print('Please login')


def view_all_slots(day, list_of_slots):

    list_of_times = []
    base_time = datetime(int(datetime.today().strftime("%Y")), int(
        datetime.today().strftime("%m")), int(datetime.today().strftime("%d")), 8, 30)

    list_of_times = [{"Date": day, "Time": (base_time + timedelta(minutes=x)).strftime(
        r'%H:%M:%S'), "Description": "----"} for x in range(0, 481, 30)]

    slots = []
    for item in list_of_slots:
        if day == item['Date']:

            slots.append(
                {"Date": item['Date'],
                 "Time": item['Time'],
                 "Description": item['Description']})

    for i in slots:
        for j in list_of_times:
            if i["Time"].split('-')[0].strip() == j['Time'] and i["Date"] == j['Date']:
                list_of_times.insert(list_of_times.index(
                    j), {"Date": i['Date'], "Time": i['Time'], "Description": i['Description']})
                list_of_times.pop(list_of_times.index(j))
    return list_of_times


def call_api(service, cID, agent):

    # Call the Calendar API
    now = datetime.today().strftime(r"%Y-%m-%dT%H:%M:%SZ")
    end = (datetime.today() + timedelta(days=7)
           ).strftime(r"%Y-%m-%dT%H:%M:%SZ")

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

    secret_json = os.getcwd()+'/credentials.json'
    clinix = 'codeclinix@gmail.com'
    user_calendar = "primary"
    service = build('calendar', 'v3', credentials=get_credentials(secret_json))
    fetch_calendar_events(call_api(service, clinix, 'clinix'), 'clinix')
    fetch_calendar_events(
        call_api(service, user_calendar, 'student'), 'student')


def volunteer_slot(agent):
    if os.path.exists(f'{agent}.csv'):
        with open(f'{agent}.csv', 'r') as events_list:
            read_data('clinix')
            create_volunteer(username)
    else:
        print('User not logged in')


def book_slot(agent):
    if os.path.exists(f'{agent}.csv'):
        with open(f'{agent}.csv', 'r') as events_list:
            read_data('clinix')
            create_booking()
    else:
        print('User not logged in')


def create_combined_csv(student_events, clinix_events):
    """
    Creates a combined csv file which stores the data of the users personal calendar and the clinix calendar
    """
    if os.path.exists(f'{student_events}.csv'):
        list_of_slots = []
        with open(f'{student_events}.csv', 'r') as file:
            student_csv_reader = (csv.DictReader(file))

            list_of_slots = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                              .split('\t')[0].strip(),
                              "Time": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                              .split('\t')[1].strip(),
                              "Description": row['DATE\t\t\tTIME\t\t\t\t\tDESCRIPTION']
                              .split('\t')[2].strip()} for row in student_csv_reader]

        with open(f'{clinix_events}.csv', 'r') as file:
            clinix_csv_reader = (csv.DictReader(file))

            list_of_slots_clinix = [{"Date": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split('\t')[0].strip(),
                                     "Time": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split('\t')[1].strip(),
                                     "ID": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split('\t')[2].strip(),
                                     "Description": row['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split('\t')[4].strip()} for row in clinix_csv_reader]

        for student_ in list_of_slots:
            for clinix_ in list_of_slots_clinix:
                if student_['Time'] == clinix_['Time'] and student_['Description'] == clinix_['Description']:
                    print("where is this: ", list_of_slots.pop(
                        list_of_slots.index(student_)))

        print("show me this:", *list_of_slots, sep='\n')
        # list_of_slots.append(list_of_slots)
        # result =  [{x['Date'], x['Time'], x['Description']} for x in list_of_slots + list_of_slots}].values()
        result2 = [x for x in list_of_slots + list_of_slots_clinix]

        result = sorted(list(result2), key=lambda i: (i['Date'], i['Time']))

        with open('combined_calendar_list.csv', 'w') as calendar:
            line = csv.writer(calendar, delimiter='\t',
                              quoting=csv.QUOTE_NONE, escapechar='\t')
            # line.writerow(['DATE', '\tTIME', '\t\tDESCRIPTION'])
            line.writerow(['DATE', '\tTIME', '\t\tID', '\t\t\tDESCRIPTION'])
            for item in result:
                error_description = item['Description']
                error_date = item['Date']
                error_time = item['Time']

                if item.get('ID', None) == None:
                    line.writerow([item['Date']+"   ",  item['Time']+"   ",
                                   "--------------------------"+"   ", item['Description']])
                else:
                    line.writerow(
                        [item['Date']+"   ", item['Time']+"   ", item['ID']+"   ", item['Description']])
                    # continue

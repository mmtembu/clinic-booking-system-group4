import os
import sys
import csv
import importlib
import time as t
import uuid
import json
from collections import defaultdict
from datetime import datetime, timedelta, time
calendar_sync = importlib.import_module('calendar_sync')
cal_setup = importlib.import_module('create_volunteer.cal_setup')


calendar_s = sys.path.append("../calendar_sync.py")
interface_s = sys.path.append("../interface.py")


hour_adjustment = -2


def time_start(time, mins):
    """
    Converts the start time of the event
    """
    new_time = cal_setup.convert_to_RFC_datetime(time[0], time[1], time[2],
                                                 time[3] + hour_adjustment, time[4], mins)
    return new_time


def time_end(time, mins):
    """
    Converts the end time of the event
    Adds 30 minutes after the start time
    """
    new_time = cal_setup.convert_to_RFC_datetime(
        time[0], time[1], time[2], time[3] + hour_adjustment, time[4], mins)
    return new_time


def get_date_and_time():
    """
    This is to validate that the correct date and time being entered
    """
    while True:
        date = input('Please enter a day you want to volunteer for? [YYYY-MM-DD] ')
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid date format eg. '2020-11-21' ")
            continue

    while True:
        time = input('Please enter a time you want to volunteer for? [Hour:Minute:Second] ')
        try:
            if time != datetime.strptime(time, "%H:%M:%S").strftime('%H:%M:%S'):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid date format eg. '13:00:00' ")
            continue

    return date, time


def loading_animation():
    """
    Creates an animation while event is being loaded
    """

    animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        t.sleep(0.3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()

    print("\n")


def is_slot_booked(day, time):

    calendar_sync.get_calendars()
    #|-------------Double Booking Check-------------|
    with open(f'{os.getcwd()}/clinix.json') as clinix_reader:
        reader = json.load(clinix_reader)
        
        # save_event_id = None
        for item in reader['info']:
            if day == item['DATE'] and time == item['TIME'].split('-')[0].strip():
                return True
        return False

        
        # gets event details (getting the clinician's emails)
        # if save_event_id != None:
        #     event_result = service.events().get(
        #         calendarId='codeclinix@gmail.com',
        #         eventId=save_event_id,
        #     ).execute()
        # else:
        #      print("No event there, please choose a selected slot or update the calendar")
        #      return None


def create_col_dict():

    """
        Creates default dict of two keys, [id, time] and sets them to '---------' which represents not empty slot
    """

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


def convert_to_proper_time(day, time):
    return (int(day.split('-')[0]), int(day.split('-')[1]), int(day.split('-')[2]), \
<<<<<<< HEAD
        int(time.split(':')[0]), int(time.split(':')[1]))


def create_volunteer(username):
=======
        int(time.split(':')[0]), int(time.split(':')[1]))    
def create_volunteer():
>>>>>>> dbebf6cef159dca73b3263d53d79d10d57313d73
    """
    Creates 3 volunteer slots (which are in 30 minute intervals) for the clinician 
    """

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()
    unique_uuid = uuid.uuid4().hex

    # start_time = (int(day.split('-')[0]), int(day.split('-')[1]), int(
    #     day.split('-')[2]), int(time.split(':')[0]), int(time.split(':')[1]))
    start_time = convert_to_proper_time(day, time)
    description = input("Which topic do you want to tutor? ")

    username = ''
    with open(os.getcwd()+'/TempData/temp.txt') as temp_file:
        username = temp_file.readline()

    username = username.split('\n')[0]

    if not is_slot_booked(day, time):
        
        col_for_events = create_col_dict()
        block_id = 0
        for col_id, col_time in col_for_events:
            if time == col_time:
                block_id = col_id
        
        list_of_times = [col_time for col_id, col_time in col_for_events if block_id == col_id]

        event_body_one = {
            "summary": "Clinix session: "+description,
            "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
            # "start": {"dateTime": time_start(start_time, 0), "timeZone": 'Africa/Johannesburg'},
            "start": {"dateTime": time_start(convert_to_proper_time(day, list_of_times[0]), 0), "timeZone": 'Africa/Johannesburg'},
            "end": {"dateTime": time_end(convert_to_proper_time(day, list_of_times[0]), 30), "timeZone": 'Africa/Johannesburg'},
            "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
            "anyoneCanAddSelf": False,
            'maxAttendees': 2,
            'sendNotifications': True,
            'sendUpdates': 'all',
            "colorId": '2'}

        event_body_two = {
            "summary": "Clinix session: "+description,
            "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
            "start": {"dateTime": time_start(convert_to_proper_time(day, list_of_times[1]), 0), "timeZone": 'Africa/Johannesburg'},
            "end": {"dateTime": time_end(convert_to_proper_time(day, list_of_times[1]), 30), "timeZone": 'Africa/Johannesburg'},
            "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
            "anyoneCanAddSelf": False,
            'maxAttendees': 2,
            'sendNotifications': True,
            'sendUpdates': 'all',
            "colorId": '2'}

        event_body_three = {
            "summary": "Clinix session: "+description,
            "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
            "start": {"dateTime": time_start(convert_to_proper_time(day, list_of_times[2]), 0), "timeZone": 'Africa/Johannesburg'},
            "end": {"dateTime": time_end(convert_to_proper_time(day, list_of_times[2]), 30), "timeZone": 'Africa/Johannesburg'},
            "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
            "anyoneCanAddSelf": False,
            'maxAttendees': 2,
            'sendNotifications': True,
            'sendUpdates': 'all',
            "colorId": '2'}

        print("\n")
        print("Loading...")
        loading_animation()

        event_result = service.events().insert(
            calendarId='codeclinix@gmail.com', body=event_body_one).execute()
        print("Event one ID: ", event_result['id'])

        event_result = service.events().insert(
            calendarId='codeclinix@gmail.com', body=event_body_two).execute()
        print("Event two  ID: ", event_result['id'])

        event_result = service.events().insert(
            calendarId='codeclinix@gmail.com', body=event_body_three).execute()
        print("Event three ID: ", event_result['id'])

        print("Slot Created  (•‿•)")
        print("Summary: ", event_result['summary'])
        calendar_sync.get_calendars()
    else:
        print("Unfortunately that slot has been taken.")


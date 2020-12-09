import os
import sys
import csv
import importlib
import time as t
import uuid
import json
from datetime import datetime, timedelta, time

cal_setup = importlib.import_module('create_volunteer.cal_setup')

# from cal_setup import get_calendar_service
# from cal_setup import convert_to_RFC_datetime as dt

calendar_s = sys.path.append("../calendar_sync.py")
interface_s = sys.path.append("../interface.py")


hour_adjustment = -2


def time_start(time, mins):
    new_time = cal_setup.convert_to_RFC_datetime(time[0], time[1], time[2],
                                                 time[3] + hour_adjustment, time[4], mins)
    return new_time


def time_end(time, mins):
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


def create_volunteer(username):

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()
    unique_uuid = uuid.uuid4().hex

    start_time = (int(day.split('-')[0]), int(day.split('-')[1]), int(
        day.split('-')[2]), int(time.split(':')[0]), int(time.split(':')[1]))
    start = time_start(start_time, 0)
    end = time_end(start_time, 30)
    description = input("Which topic do you want to tutor? ")

    username = ''
    with open(os.getcwd()+'/TempData/temp.txt') as temp_file:
        username = temp_file.readline()

    username = username.split('\n')[0]

    first = datetime.strptime(
        (day+'T'+time), r'%Y-%m-%dT%H:%M:%S')

    event_body_one = {
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
        "start": {"dateTime": time_start(start_time, 0), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 30), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": False,
        'maxAttendees': 2,
        'sendNotifications': True,
        'sendUpdates': 'all',
        "colorId": '2'}

    event_body_two = {
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
        "start": {"dateTime": time_start(start_time, 30), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 60), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": False,
        'maxAttendees': 2,
        'sendNotifications': True,
        'sendUpdates': 'all',
        "colorId": '2'}

    event_body_three = {
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"\n' + unique_uuid,
        "start": {"dateTime": time_start(start_time, 60), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 90), "timeZone": 'Africa/Johannesburg'},
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



def do_delete():
    """
    Used to delete specific volunteer slots on calendar
    """
    
    day, time = get_date_and_time()
    
    with open('clinix.json') as calendar:
        clinix_reader = json.load(calendar)
    
        for item in clinix_reader['info']:
            error_description = item['Description']
            error_date = item['Date']
            error_time = item['Time']

            if item.get('ID', None) == None:
                line.writerow([item['Date']+"   ",  item['Time']+"   ",
                               "--------------------------"+"   ", item['Description']])



    service = cal_setup.get_calendar_service()
    if create_booking and delete is True:
        service.events().delete(calendarId, event_result['id']).execute()
    else:
        do_help()



# if __name__ == '__main__':
#    create_booking() 

import time
import sys
import json
import os
import csv
import importlib
from datetime import datetime
from datetime import datetime, timedelta
import make_booking.cal_setup
from make_booking.cal_setup import get_calendar_service
calendar_sync = importlib.import_module('calendar_sync')

def get_date_and_time():
    """
    time = input('Please enter a time you want to volunteer for? [00:00:00] ')	    This is to validate that the correct date and time being entered
    """
    while True:
        date = input(
            'Please enter a day you want to book for? [YYYY-MM-DD] ')
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid date format eg. '2020-11-21' ")
            continue

    while True:
        time = input(
            'Please enter a time you want to book for? [Hour:Minute:Second] ')
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

    animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]",
                 "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

    for i in range(len(animation)):
        time.sleep(0.3)
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\n")


def create_booking():
    """
    function creates a booking on already existing volunteer slots,
    used by patient to book clinicians
    """

    username = ''
    with open(os.getcwd()+'/TempData/temp.txt') as temp_file:
        username = temp_file.readline()
    username = username.split('\n')[0]
    service = get_calendar_service()

    data_api_time = []
    with open(f'clinix.json') as clinix_calendar:
        clinix_calendar_reader = json.load(clinix_calendar)
        for item in clinix_calendar_reader['info']:
            event_id = item['ID']
            start_time = item['TIME'].split('-')[0].strip()
            start_date = item['DATE']

            data_api_time.append((f'{start_date}T{start_time}', event_id))

    date_input, time_input = get_date_and_time()

    save_event_id = ''
    for item in data_api_time:
        if item[0].split('T')[0] == date_input and item[0].split('T')[1] == time_input:
            save_event_id = item[1]
            break

    # gets event details (getting the clinician's emails)
    event_result = service.events().get(
        calendarId='codeclinix@gmail.com',
        eventId=save_event_id,
    ).execute()

    attendee_details = None
    attendee_email = None

    try:
        attendee_details = event_result['attendees'][0]
        attendee_email = attendee_details.get('email')

        if len(event_result['attendees']) == 1:

            if username == event_result['attendees'][0].get('email').split('@')[0]:
                print("Cannot book a slot you've volunteered for.")
            else:
                event_result = service.events().patch(
                    calendarId='codeclinix@gmail.com',
                    eventId=save_event_id,
                    body={
                        "attendees": [{'email': attendee_email}, {'email': username+'@student.wethinkcode.co.za'}],
                        'sendNotifications': True
                    },
                ).execute()

                print("\n")
                print("Loading...")
                loading_animation()
                print("Booking Successful   (•‿•) ")
                print("Id: ", event_result['id'])
                print(event_result['summary'])
                calendar_sync.get_calendars()

        elif len(event_result['attendees']) == 2:

            attendee_details = event_result['attendees'][1]
            attendee_email = attendee_details.get('email')
            if username == attendee_email.split('@')[0].strip():
                print("You've already booked a slot.")
            elif username == event_result['attendees'][0].get('email').split('@')[0]:
                print("Cannot book a slot you've volunteered for.")
            elif username != attendee_email.split('@')[0].strip():
                print("Someone already booked for that slot.")

    except KeyError:
        print("There's no event there.")

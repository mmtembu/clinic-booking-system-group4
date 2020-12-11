import os
import sys
import csv
import importlib
import time as t
import json
from datetime import datetime, timedelta, time
calendar_sync = importlib.import_module('calendar_sync')
cal_setup = importlib.import_module('cancel_volunteer.cal_setup')

def get_date_and_time():
    """
    This is to validate that the correct date and time being entered
    """
    while True:
        date = input('Please enter the day you want to cancel slot? [YYYY-MM-DD] ')
        try:
            if date != datetime.strptime(date, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid date format eg. '2020-11-21' ")
            continue

    while True:
        time = input('Please enter the time you want to cancel slot? [Hour:Minute:Second] ')
        try:
            if time != datetime.strptime(time, "%H:%M:%S").strftime('%H:%M:%S'):
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid date format eg. '13:00:00' ")
            continue

    return date, time


def cancel_volunteer():
    """
    Deletes all 3 volunteer slots the clinician has signed up for
    """

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()

    with open('clinix.json') as clinix_calendar_reader:
        reader = json.load(clinix_calendar_reader)
        id_of_event = None
        events = []
        save_event_id = ''
        for item in reader['info']:
            if day == item['DATE'] and time == item['TIME'].split('-')[0].strip():
                id_of_event = item['SUMMARY'].split('\n')[1].strip()
    
        for item in reader['info']:
            if id_of_event != None:
                if id_of_event == item['SUMMARY'].split('\n')[1].strip():
                    save_event_id = item['ID']
                    events.append(item['ID'])
            else:
                print("No event there, please choose a selected slot or update the calendar")
                return None
        
        with open(os.getcwd()+"/TempData/temp.txt") as user_file:
            username = user_file.read()
            email = username+'@student.wethinkcode.co.za'
            
        # gets event details (getting the clinician's emails)
        event_result = service.events().get(
            calendarId='codeclinix@gmail.com',
            eventId=save_event_id,
        ).execute()

        attendee_details = event_result['attendees'][0]
        attendee_email = attendee_details.get('email')
        if attendee_email == email:

            print("Loading...")
            loading_animation()

            #deletes all 3 events usng an api request
            service = cal_setup.get_calendar_service()
            service.events().delete(calendarId='codeclinix@gmail.com',eventId=events[0]).execute()
            service.events().delete(calendarId='codeclinix@gmail.com',eventId=events[1]).execute()
            service.events().delete(calendarId='codeclinix@gmail.com',eventId=events[2]).execute()

            print("Slot Deleted  (•‿•)")
            calendar_sync.get_calendars()

        else:
            print("Unauthorized email/username, only signed in user can delete the event.")


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
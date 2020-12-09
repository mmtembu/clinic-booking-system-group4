import os
import sys
import csv
import importlib
import time as t
import json
from datetime import datetime, timedelta, time
cal_setup = importlib.import_module('cal_setup')

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


def cancel_booking():

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()

    username = ''
    with open('TempData/temp.txt', 'r') as username_in_file:
        
        # service = cal_setup.get_calendar_service()
        username = username_in_file.read()
    
    with open('clinix.json') as clinix_reader:
        events = []
        reader = json.load(clinix_reader)
        
        for item in reader['info']:
            if day == item['DATE'] and time == item['TIME'].split('-')[0].strip():
                if len(item['ATTENDEES']) > 1:
                    events.append(item['ATTENDEES'])
        
            # gets event details (getting the clinician's emails)
            event_result = service.events().get(
                calendarId='codeclinix@gmail.com',
                eventId=save_event_id,
            ).execute()

            if username == event_result['attendees'][1]:
                
            attendee_details = event_result['attendees'][1]
            attendee_email = attendee_details.get('email')        
        service.events().delete(calendarId='codeclinix@gmail.com',eventId=events[0]).execute()

        # # First retrieve the event from the API.
        # event = service.events().get(calendarId='codeclinix@gmail.com', eventId='eventId').execute()

        # event['summary'] = 'Appointment at Somewhere'

        # updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

        # # Print the updated date.
        # print(updated_event['updated'])

cancel_booking()
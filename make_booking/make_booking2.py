import sys
import importlib
from datetime import datetime, timedelta, time
cal_setup =  importlib.import_module('make_booking.cal_setup')

# from cal_setup import get_calendar_service
# from cal_setup import convert_to_RFC_datetime as dt

calendar_s = sys.path.append("../calendar_sync.py")
import os
# from calendar_sync import get_username
# from importlib import import_module
# from . import calendar_sync
# calendar_s = import_module('calendar_sync')

'''filepath = "//goinfre//kkara//problems//Group Project//clinic-booking-system-group4//calendar_sync.py"
os.path.basename(filepath)
print(os.path.basename(your_path))'''

available_slots = [(2020,11,10,13,0),(2020,11,10,14,0)]
hour_adjustment = -2
# username = calendar_s.get_username()


def print_slots():
    """
    Prints all available slots
    """
    print("Available slots are: ")
    for i in range(len(available_slots)):
       print(str(i+1)+'. ', end='')
       print(available_slots[i])


def slot_input():
    """
    Takes input for slot, making sure its a valid integer
    """
    while True:
        try:
            chosen_slot = int(input("Please select slot (Insert number only): "))
            if chosen_slot <= 0:
                print("Please insert a Positive Integer")
                continue
            try:
                available_slots[chosen_slot - 1]
                break
            except IndexError:
                print("Please use the numbers shown on the available slots list")
        except ValueError:
            print("Please insert a Valid Integer")

    return chosen_slot - 1

def time_start(time):
    new_time = dt(time[0],time[1],time[2],time[3] + hour_adjustment,time[4])
    return new_time

def time_end(time):
    new_time = dt(time[0],time[1],time[2],time[3]+ hour_adjustment,time[4] + 30)
    return new_time

def create_booking(username):
   
    service = cal_setup.get_calendar_service()

    print_slots()
    num = slot_input()
    start_time = available_slots[num]
    start = time_start(start_time)
    end = time_end(start_time)
    description = input("What do you need help with? ")

    event_result = service.events().insert(calendarId='primary',
       body={
           "summary": 'Code Clinics Session',
           "description": 'Patient needs help with: "'+description+'"',
           "start": {"dateTime": start, "timeZone": 'Africa/Johannesburg'},
           "end": {"dateTime": end, "timeZone": 'Africa/Johannesburg'},
           "attendees": [{'email': username+'@student.wethinkcode.co.za'}],
           "anyoneCanAddSelf": True,
           'maxAttendees' : 2,
           "colorId": '2'
       }
   ).execute()

    print("Created event")
    print("ID: ", event_result['id'])
    print("Summary: ", event_result['summary'])
    print("Starts at: ", event_result['start']['dateTime'])
    print("Ends at: ", event_result['end']['dateTime'])

# if __name__ == '__main__':
#    create_booking()
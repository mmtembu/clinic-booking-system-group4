import os
import sys
import importlib
from datetime import datetime, timedelta, time
cal_setup = importlib.import_module('make_booking.cal_setup')

# from cal_setup import get_calendar_service
# from cal_setup import convert_to_RFC_datetime as dt

calendar_s = sys.path.append("../calendar_sync.py")
interface_s = sys.path.append("../interface.py")

available_slots = [(2020, 11, 10, 13, 0), (2020, 11, 10, 14, 0)]
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
            chosen_slot = int(
                input("Please select slot (Insert number only): "))
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
    time = input('Please enter a time you want to volunteer for? [00:00:00] ')	    This is to validate that the correct date and time being entered
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


def create_booking(username):

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()

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
        "description": 'Patient needs help with: "'+description+'"',
        "start": {"dateTime": time_start(start_time, 0), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 30), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": True,
        'maxAttendees': 2,
        "colorId": '2'}

    event_body_two = {
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"',
        "start": {"dateTime": time_start(start_time, 30), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 60), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": True,
        'maxAttendees': 2,
        "colorId": '2'}

    event_body_three = {
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"',
        "start": {"dateTime": time_start(start_time, 60), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": time_end(start_time, 90), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": True,
        'maxAttendees': 2,
        "colorId": '2'}

    event_result = service.events().insert(
        calendarId='codeclinix@gmail.com', body=event_body_one).execute()
    print("Event one ID: ", event_result['id'])

    event_result = service.events().insert(
        calendarId='codeclinix@gmail.com', body=event_body_two).execute()
    print("Event two  ID: ", event_result['id'])

    event_result = service.events().insert(
        calendarId='codeclinix@gmail.com', body=event_body_three).execute()
    print("Event three ID: ", event_result['id'])

    print("Created event")
    print("Summary: ", event_result['summary'])
    print("Starts at: ", event_result['start']['dateTime'])
    print("Ends at: ", event_result['end']['dateTime'])


    def do_delete()
    """
    Used to delete specific volunteer slots on calendar
    """

    if delete is True:
        service.events().delete(calendarId, event_result['id']).execute()
    else:
        do_help() 


def cancel_volunteer_slots(calendarId, event_result)
    """ Will delete booking for both parties
    """
    if create_booking and delete is True:
        do_delete()

# if __name__ == '__main__':
#    create_booking()

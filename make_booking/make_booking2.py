import os
import sys
import importlib
from datetime import datetime, timedelta, time
cal_setup = importlib.import_module('make_booking.cal_setup')

# from cal_setup import get_calendar_service
# from cal_setup import convert_to_RFC_datetime as dt

calendar_s = sys.path.append("../calendar_sync.py")
interface_s = sys.path.append("../interface.py")
# from calendar_sync import get_username
# from importlib import import_module
# from . import calendar_sync
# calendar_s = import_module('calendar_sync')

'''filepath = "//goinfre//kkara//problems//Group Project//clinic-booking-system-group4//calendar_sync.py"
os.path.basename(filepath)
print(os.path.basename(your_path))'''

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
    date = input('Please enter a day you want to volunteer for? [yyyy-mm-dd] ')
    time = input('Please enter a time you want to volunteer for? [00:00:00] ')
    return date, time


def create_booking(username):

    service = cal_setup.get_calendar_service()
    day, time = get_date_and_time()

    start_time = (int(day.split('-')[0]), int(day.split('-')[1]), int(
        day.split('-')[2]), int(time.split(':')[0]), int(time.split(':')[1]))
    start = time_start(start_time, 0)
    end = time_end(start_time, 30)
    # description = input("What do you need help with? ")
    description = input("Which topic do you want to tutor? ")

    username = ''
    with open(os.getcwd()+'/TempData/temp.txt') as temp_file:
        username = temp_file.readline()

    username = username.split('\n')[0]

    # list_of_times = [{"Date": day, "Time": (base_time + timedelta(minutes=x)).strftime(
    #     r'%H:%M:%S'), "Description": "----"} for x in range(0, 481, 30)]

    # (base_time + timedelta(minutes=x)).strftime(
    #     r'%H:%M:%S')

    # print('show me the: ', datetime.strptime(
    #     (day+'T'+time), r'%Y-%m-%dT%H:%M:%S'))

    event_result = service.events().insert(calendarId='codeclinix@gmail.com', body={
        "summary": "Clinix session: "+description,
        "description": 'Patient needs help with: "'+description+'"',
        "start": {"dateTime": datetime.strptime(str(first), '%Y-%m-%d %H:%M:%S'), "timeZone": 'Africa/Johannesburg'},
        "end": {"dateTime": datetime.strptime(str(first + timedelta(hours=0, minutes=30, seconds=0)), '%Y-%m-%d %H:%M:%S'), "timeZone": 'Africa/Johannesburg'},
        "attendees": [{'email': username + '@student.wethinkcode.co.za'}],
        "anyoneCanAddSelf": True,
        'maxAttendees': 2,
        "colorId": '2'}).execute()

    first = datetime.strptime(
        (day+'T'+time), r'%Y-%m-%dT%H:%M:%S')
    x = 0
    while x < 90:
        first += timedelta(hours=0, minutes=30, seconds=0)
        x += 30

    print("Created event")
    print("ID: ", event_result['id'])
    print("Summary: ", event_result['summary'])
    print("Starts at: ", event_result['start']['dateTime'])
    print("Ends at: ", event_result['end']['dateTime'])

# if __name__ == '__main__':
#    create_booking()

import make_booking.cal_setup
import sys
import json
import os
import csv
from datetime import datetime
from datetime import datetime, timedelta
from make_booking.cal_setup import get_calendar_service


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

def create_booking():
    username = ''
    with open(os.getcwd()+'/TempData/temp.txt') as temp_file:
        username = temp_file.readline()
    username = username.split('\n')[0]
    # update the event to tomorrow 9 AM IST
    service = get_calendar_service()
    
    data_api_time = []
    with open(f'clinix.csv', 'r') as clinix_calendar:
        clinix_csv_reader = (csv.DictReader(clinix_calendar))
        for item in clinix_csv_reader:
            # print("what is in here:",item['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split())
            event_id = item['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split()[4]
            start_time = item['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split()[1]
            start_date = item['DATE\t\t\tTIME\t\t\t\t\tID\t\t\t\t\t\t\tDESCRIPTION'].split()[0]

            data_api_time.append((f'{start_date}T{start_time}', event_id))

    date_input, time_input = get_date_and_time()
    # print("show bra show me this:", data_api_time)

    save_event_id = ''
    for item in data_api_time:
        if item[0].split('T')[0] == date_input and item[0].split('T')[1] == time_input:
            save_event_id = item[1]
            break

    # print("show me the id man:", save_event_id)
    event_result = service.events().get(
        calendarId='codeclinix@gmail.com',
        eventId=save_event_id,
    ).execute()

    # print(event_result['maxAttendees'])
    attendee_details = event_result['attendees'][0]
    attendee_email = attendee_details.get('email')
    # print(attendee_email)

    event_result = service.events().patch(
          calendarId='codeclinix@gmail.com',
          eventId=save_event_id,
          body={
           "attendees": [{'email': attendee_email}, {'email': username+'@student.wethinkcode.co.za'}]
           },
        ).execute()


    print("updated event")
    print("id: ", event_result['id'])
    print(event_result['summary'])
    print(event_result['attendees'])


if __name__ == '__main__':
    main()

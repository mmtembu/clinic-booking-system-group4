
import sys
from interface import create_profile,  get_user_info
from calendar_sync import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
 

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    get_calendars()

    # call_calendars('primary', 'student')
    # call_calendars('codeclinix@gmail.com', 'clinix')


def do_help():
    """Lists all the available commands"""
    print("""
  HELP       -   lists all the available commands the booking system provides
  BOOKING    -   allows a student to make a booking to an available slot
  CLINICIANS -   allows the student to view all the available clinicians
  CLINIX     -   shows coding clinix calendar events
  LOGIN      -   initializes the clinix calendar
  LOGOUT     -   use this command to remove your credentials from current system
          """)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if sys.argv[1].upper() == 'HELP':
            do_help()
        elif sys.argv[1].upper() == 'INIT':
            create_profile()
        elif sys.argv[1].upper() == 'LOGIN':
            main()
        elif sys.argv[1].upper() == 'VIEW_CALENDAR':
            print('Which calendar do you want?\n1. Your calendar\n2. Clinix Calendar\n')
            num = input('which calendar do you want?[choose number] ')
            print()
            while not num.isnumeric() or int(num) > 2 or int(num) < 1:
                num = input('which calendar do you want?[choose number] ')
            if num == '1':
                read_data('student')
            elif num == '2':
                read_data('clinix')
            print()
    elif len(sys.argv) == 1:
        do_help()

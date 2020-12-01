
import sys
from interface import create_profile,  get_user_info, is_logged_in, logout
from calendar_sync import get_calendars, read_data, volunteer_slot, book_slot, create_combined_csv
from create_volunteer import create_volunteer_slot
from create_volunteer.create_volunteer_slot import do_delete

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    get_calendars()
    # print(get_both_calendars())
    # username = get_username()
    # make_booking2.create_booking(username)

#   CLINICIANS    -   allows the student to view all the available clinicians
#   CLINIX        -   shows coding clinix calendar events
#   BOOKING       -   allows a student to make a booking to an available slot


def do_help():
    """Lists all the available commands"""
    print("""
HELP          -   lists all the available commands the booking system provides
LOGIN         -   initializes the clinix calendar
LOGOUT        -   use this command to remove your credentials from current
                  system
VIEW_CALENDAR -   shows list of calendars you can view
MAKE_BOOKING  -   makes the booking for the patient
""")


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1].upper() == 'HELP':
            do_help()
        elif sys.argv[1].upper() == 'INIT':
            create_profile()
        elif sys.argv[1].upper() == 'LOGIN':
            main()
        elif sys.argv[1].upper() == 'LOGOUT':
            logout()
        elif sys.argv[1].upper() == 'MAKE_BOOKING':
            book_slot('clinix')
        elif sys.argv[1].upper() == 'VIEW_CALENDAR':
            print(
                'Which calendar do you want?\n1. Your calendar\n2. Clinix Calendar\n3. Volunteer Slot\n4. Cancel Volunteer Slot\n')
            num = input('which calendar do you want?[choose number] ')
            print()
            create_combined_csv('student', 'clinix')

            while not num.isnumeric() or int(num) > 4 or int(num) < 1:
                num = input('Which calendar do you want?[choose number] ')
            if num == '1':
                read_data('student')
            elif num == '2':
                read_data('clinix')
            elif num == '3':
                volunteer_slot('clinix')
            elif num == '4':
                do_delete()

            print()
        else:
            do_help()
    elif len(sys.argv) == 1:
        do_help()

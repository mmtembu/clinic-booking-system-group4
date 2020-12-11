import sys
from interface import create_profile,  get_user_info, is_logged_in, logout
from calendar_sync import get_calendars, read_data, volunteer_slot, book_slot, create_combined_csv, cancel_slot, cancel_book
from create_volunteer import create_volunteer_slot
from cancel_volunteer.cancel_volunteer_slot import cancel_volunteer


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 7 events on the user's calendar.
    Does this whenever someone logs in (also updates calendar)
    """

    get_calendars()



def do_help():
    """Lists all the available commands"""
    print("""
HELP          -   lists all the available commands the booking system provides
LOGIN         -   initializes the clinix calendar (also updates calendar)
LOGOUT        -   use this command to remove your credentials from current
                  system
VIEW_CALENDAR -   shows list of calendars you can view
MAKE_BOOKING  -   makes the booking for the patient
CREATE_SLOT   -   creates a set of 3 volunteer slots for the clinician
CANCEL_BOOKING -  cancels booking for the patient
CANCEL_SLOT   -   cancels volunteer slots for the clinician

PS. Please login again to refresh the calendar
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
        elif sys.argv[1].upper() == 'CREATE_SLOT':
            volunteer_slot('clinix')
        elif sys.argv[1].upper() == 'CANCEL_BOOKING':
            cancel_book('clinix')
        elif sys.argv[1].upper() == 'CANCEL_SLOT':
            cancel_slot('clinix')
        

        elif sys.argv[1].upper() == 'VIEW_CALENDAR':
            print(
                'Which calendar do you want?\n1. Your calendar\n2. Clinix Calendar\n')
            num = input('Which calendar do you want?[choose number] ')
            print()
            create_combined_csv('student', 'clinix')

            while not num.isnumeric() or int(num) > 4 or int(num) < 1:
                num = input('Which calendar do you want?[choose number] ')
            if num == '1':
                read_data('student')
            elif num == '2':
                read_data('clinix')

            print()
        else:
            do_help()
    elif len(sys.argv) == 1:
        do_help()

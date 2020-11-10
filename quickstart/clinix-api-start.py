from __future__ import print_function
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import datetime
import pickle
import os.path
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from interface import create_profile
# import using_selenium


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    flow = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)

            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def do_selenium(url, flow):

    print('Enter the gmailid and password')
    gmailId, passWord = map(str, input().split())
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())

        driver.get(url)
        driver.implicitly_wait(15)

        # tabIndex = driver.find_element_by_partial_link_text(
        #     '@student.wethinkcode.co.za')
        tabIndex = driver.find_elements(
            By.CSS_SELECTOR, "[data-email*='@student.wethinkcode.co.za']")
        tabIndex.click()

        loginBox = driver.find_element_by_xpath('//*[@id ="identifierId"]')
        loginBox.send_keys(gmailId)

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="identifierNext"]')
        nextButton[0].click()

        passWordBox = driver.find_element_by_xpath(
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(passWord)

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="passwordNext"]')
        nextButton[0].click()

        nextButton = driver.find_elements_by_xpath(
            '//*[@id ="submit_approve_access"]')
        nextButton[0].click()

        print('Login Successful...!!')
    except:
        print('Login Failed')
    return url


# if __name__ == "__main__":


def do_help():
    """Lists all the available commands"""
    print("""
  HELP       -   lists all the available commands the booking system provides
  BOOKING    -   allows a student to make a booking to an available slot
  CLINICIANS -   allows the student to view all the available clinicians
          """)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1].upper() == 'HELP':
            do_help()
        elif sys.argv[1].upper() == 'INIT':
            create_profile()
        elif sys.argv[1].upper() == 'START':
            main()
    elif len(sys.argv) == 1:
        do_help()

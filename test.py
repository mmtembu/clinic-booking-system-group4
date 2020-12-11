import json
import os
import unittest
from unittest.main import main
from test_base import captured_io
from io import StringIO
from unittest.mock import patch
import cancel_volunteer.cancel_volunteer_slot as cancel_volunteer
import create_volunteer.create_volunteer_slot as create_volunteer
import make_booking.make_booking as make_booking
import cancel_booking.cancel_booking as cancel_booking


# data = {}
# data['info'] = []

# data['info'].append({
#     'species' : 'human',
#     'name' : 'mangaliso',
#     'address' : '839 bluegum street',
#     'gender' : 'male'
# })

# data['info'].append({
#     'species' : 'moncalamari',
#     'name' : 'stowza',
#     'address' : '45 loveday street',
#     'gender' : 'male'
# })

# with open(os.getcwd()+'/info.json', 'w') as outfile:
#     json.dump(data, outfile)

class TestCaseVolunteer(unittest.TestCase):

    @patch("sys.stdin", StringIO("2020-12-28\n13:00:00\n"))
    def test_time_validation_cancel_volunteer_pass(self):
        self.assertEqual(cancel_volunteer.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    @patch("sys.stdin", StringIO("2020-13-32\n27:61:00\n2020-12-28\n13:00:00\n"))
    def test_time_validation_cancel_volunteer_passandthenfail(self):
        self.assertEqual(cancel_volunteer.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    def test_time_validation_cancel_volunteer_fail(self):
        with captured_io(StringIO('2020-13-32\n2020-12-28\n27:00:00\n13:00:00\n')) as (out, err):
            cancel_volunteer.get_date_and_time()

        str1 = "Please enter a day you want to volunteer for? [YYYY-MM-DD] "
        str2 = "Please enter a valid date format eg. '2020-11-21' "+"\n"
        str3 = "Please enter a day you want to volunteer for? [YYYY-MM-DD] "
        str4 = "Please enter a time you want to volunteer for? [Hour:Minute:Second] "
        str5 = "Please enter a valid date format eg. '13:00:00' "
        str6 = str1 + str2 + str3 + str4 + str5

        output = out.getvalue().strip()

        self.assertEqual(str6, output[:285])


    @patch("sys.stdin", StringIO("2020-12-28\n13:00:00\n"))
    def test_time_validation_create_volunteer_pass(self):
        self.assertEqual(create_volunteer.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    @patch("sys.stdin", StringIO("2020-13-32\n27:61:00\n2020-12-28\n13:00:00\n"))
    def test_time_validation_create_volunteer_passandthenfail(self):
        self.assertEqual(create_volunteer.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    def test_time_validation_create_volunteer_fail(self):
        with captured_io(StringIO('2020-13-32\n2020-12-28\n27:00:00\n13:00:00\n')) as (out, err):
            create_volunteer.get_date_and_time()

        str1 = "Please enter a day you want to volunteer for? [YYYY-MM-DD] "
        str2 = "Please enter a valid date format eg. '2020-11-21' "+"\n"
        str3 = "Please enter a day you want to volunteer for? [YYYY-MM-DD] "
        str4 = "Please enter a time you want to volunteer for? [Hour:Minute:Second] "
        str5 = "Please enter a valid date format eg. '13:00:00' "
        str6 = str1 + str2 + str3 + str4 + str5

        output = out.getvalue().strip()

        self.assertEqual(str6, output[:285])

class TestCaseBooking(unittest.TestCase):

    @patch("sys.stdin", StringIO("2020-12-28\n13:00:00\n"))
    def test_time_validation_cancel_booking_pass(self):
        self.assertEqual(cancel_booking.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    @patch("sys.stdin", StringIO("2020-13-32\n27:61:00\n2020-12-28\n13:00:00\n"))
    def test_time_validation_cancel_booking_passandthenfail(self):
        self.assertEqual(cancel_booking.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    def test_time_validation_cancel_booking_fail(self):
        with captured_io(StringIO('2020-13-32\n2020-12-28\n27:00:00\n13:00:00\n')) as (out, err):
            cancel_booking.get_date_and_time()

        str1 = "Please enter a day you want to book for? [YYYY-MM-DD] "
        str2 = "Please enter a valid date format eg. '2020-11-21' "+"\n"
        str3 = "Please enter a day you want to book for? [YYYY-MM-DD] "
        str4 = "Please enter a time you want to book for? [Hour:Minute:Second] "
        str5 = "Please enter a valid date format eg. '13:00:00' "
        str6 = str1 + str2 + str3 + str4 + str5
        print(len(str6))

        output = out.getvalue().strip()

        self.assertEqual(str6, output[:270])



    @patch("sys.stdin", StringIO("2020-12-28\n13:00:00\n"))
    def test_time_validation_make_booking_pass(self):
        self.assertEqual(make_booking.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    @patch("sys.stdin", StringIO("2020-13-32\n27:61:00\n2020-12-28\n13:00:00\n"))
    def test_time_validation_make_booking_passandthenfail(self):
        self.assertEqual(make_booking.get_date_and_time(), 
        ("2020-12-28","13:00:00"))


    def test_time_validation_make_booking_fail(self):
        with captured_io(StringIO('2020-13-32\n2020-12-28\n27:00:00\n13:00:00\n')) as (out, err):
            make_booking.get_date_and_time()

        str1 = "Please enter a day you want to book for? [YYYY-MM-DD] "
        str2 = "Please enter a valid date format eg. '2020-11-21' "+"\n"
        str3 = "Please enter a day you want to book for? [YYYY-MM-DD] "
        str4 = "Please enter a time you want to book for? [Hour:Minute:Second] "
        str5 = "Please enter a valid date format eg. '13:00:00' "
        str6 = str1 + str2 + str3 + str4 + str5
        

        output = out.getvalue().strip()

        self.assertEqual(str6, output[:270])


if __name__ == "__main__":
    unittest.main()


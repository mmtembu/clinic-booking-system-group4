import json
import os
import unittest
from unittest.main import main
from test_base import captured_io
from io import StringIO
from unittest.mock import patch
import interface
import hashlib
import cancel_volunteer.cancel_volunteer_slot as cancel_volunteer
import create_volunteer.create_volunteer_slot as create_volunteer
import make_booking.make_booking as make_booking
import cancel_booking.cancel_booking as cancel_booking


class TestInterface(unittest.TestCase):

    def test_create_profile_pass(self):
        with captured_io(StringIO('tx\njhb\ntx\ntx\n')) as (out, err):
            interface.create_profile()
        output = out.getvalue().strip()
        print(output)
        self.assertEqual("""Please enter student username: Which campus are you from: Now you can login""",output)


    def test_password_haser(self):
        pword1 = "1234"
        pword2 = "1234"

        output = hashlib.sha512(pword1.encode('utf-8')).hexdigest()
        self.assertEqual(interface.password_hasher(pword1, pword2), output)   


    # def test_password_validator(self):
    #     pword1 = "1234"
    #     pword2 = "1234"
        
    #     with open("tx.json", "r") as person:
    #         person_info = json.loads(person.read())
    #         file1  = person_info["password"]

    #     self.assertTrue(interface.password_validator(pword1, file1))


    def test_create_temp_data(self):
        if os.path.exists("temp.txt"):
            self.assertEqual(interface.create_temp_data("tx"),"""Welcome back tx""")
        else:
            self.assertTrue(interface.create_temp_data("tx"))


    def test_get_user_info(self):
        with captured_io(StringIO("tx\n1234\n")) as (out, err):
            interface.get_user_info()
        with open("tx.pickle","w") as pickle:
            pickle = ""
        with open("student.json","w") as student:
            student = {}
        with open("clinix.json","w") as clinix:
            clinix = {}
        output = out.getvalue().strip()
        self.assertEqual("""Please enter student username: Welcome back, tx""", output)

    
    def test_logout(self):
        with captured_io(StringIO("tx\n")) as (out, err):
            interface.logout()
        output = out.getvalue().strip()
        self.assertEqual("""Please enter Username you want to logout: tx successfully removed from system""", output)

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


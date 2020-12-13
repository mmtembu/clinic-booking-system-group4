import os
import unittest
from unittest.mock import patch
import sys
import json
from test_base import run_unittests
from test_base import captured_io
from io import StringIO
import hashlib
import interface

class MyTestFunction(unittest.TestCase):
    

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
   

if __name__ == '__main__':
    unittest.main()
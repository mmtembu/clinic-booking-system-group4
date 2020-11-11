import sys
import json
import os


def create_profile():
    name = ''
    if not os.path.exists("config.json"):
        while name == '':
            name = input("Please enter student username: ")
            campus = input("Which campus are you from: ")
            email = name + "@student.wethinkcode.co.za"
        with open("config.json","w") as person:
            json.dump({"name":name,"email":email,"campus":campus},person)
            return "Profile Created"
    else:
        with open("config.json") as person:
            file1  = json.load(person)
            print('configuration file exists:\n', '~/.config/clinix/config.json')
            return file1


def get_user_info():
    if os.path.exists("config.json"):
        with open("config.json") as person:
            file1  = json.load(person)
        return True, file1
    else:
        return False, "No configurations found"

# print(create_profile())
import sys
import json
import os


username = ''

def create_profile():
    global username
    username = input("Please enter student username: ")
    while not os.path.exists(f"{username}.json"):
    # while username == '':
        # username = input("Please enter student username: ")
        campus = input("Which campus are you from: ")
        email = username + "@student.wethinkcode.co.za"
        pword1 = input("please enter password: ")
        pword2 = input("please confirm password: ")

        while pword1 != pword2:
            print("password don't match : ")
            pword1 = input("please enter password: ")
            pword2 = input("please confirm password: ")
            
        with open(f"{username}.json","w") as person:
            json.dump({"username":username,"email":email,"campus":campus, "password": password_hasher(pword1, pword2)},person)
            return "Profile Created"
    else:
        with open(f"{username}.json") as person:
            file1  = json.load(person)
            print('configuration file exists:\n', '~/.config/clinix/config.json')
            return file1


def password_hasher(pword1, pword2):
    return pword1


def password_validator(pword1, file1):
    input_pass = password_hasher(pword1, pword1)
    return input_pass == file1["password"]

"TODO check pickle's expiry"
def get_user_info():
    global username
    # print('show me the username', create_profile())
    if os.path.exists(f"{username}.json"):
        with open(f"{username}.json") as person:
            if password_validator(input('Please enter password to login', person)):
                if os.path(f'{username}.pickle'):
                    return True, json.load(person)
                else:
                    return False, "Please login"
            else:
                return False, "Incorrect password"
    else:
        return False, "Use 'clinix init'"




# print(create_profile())
import sys
import json
import os


username = ''

def create_profile():
    """
    This funtion creates the users config file if one doesnt exist and 
    file path if one exist
    """
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
        with open(f"{username}.json","r") as person:
            file1  = json.load(person)
            print('configuration file exists:\n', '~/.config/clinix/config.json')
            return file1


def password_hasher(pword1, pword2):
    """
    This funtion will encrypt the password
    """
    return pword1


def password_validator(pword1, file1):
    """
    This funtion vaildates the pasword
    """
    input_pass = password_hasher(pword1, pword1)
    return input_pass == file1

"TODO check pickle's expiry"
def get_user_info():
    """
    
    """
    global username
    username = input("Please enter student username: ")
    if os.path.exists(f"{username}.json"):
        with open(f"{username}.json", "r") as person:
            person_info = json.loads(person.read())
            if password_validator(input('Please enter password to login '), person_info["password"]):
                if os.path.exists(f'{username}.pickle'):
                    print("Token expiry: ")
                    return True, person_info
                else:
                    return True, person_info
            else:
                return False, "Incorrect password"
    else:
        print("Use 'clinix init'")
        exit()
# print(create_profile())
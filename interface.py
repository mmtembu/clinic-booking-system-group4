import sys
import json
import os
import stdiomask
import hashlib
import uuid
import tempfile

# username = ''
is_logged_in = False

"""
TODO: Don't forget to account for empty strings when creating a json file and prevent init if someone is logged in
"""


def create_profile():
    """
    This funtion creates the users config file if one doesnt exist and
    file path if one exist
    """

    file1 = None
    # global username
    username = input("Please enter student username: ")
    if not os.path.exists(f"{os.getcwd()}/{username}.json"):
        # while username == '':
        # username = input("Please enter student username: ")
        campus = input("Which campus are you from: ")
        email = username + "@student.wethinkcode.co.za"
        pword1 = stdiomask.getpass("Please create a password: ")
        pword2 = stdiomask.getpass("Please confirm password: ")

        while pword1 != pword2:
            print("Password doesn't match : ")
            pword1 = stdiomask.getpass("Please create a password: ")
            pword2 = stdiomask.getpass("Please confirm password: ")

        with open(f"{username}.json", "w") as person:
            json.dump({"username": username, "email": email, "campus": campus,
                       "password": password_hasher(pword1, pword2)}, person)
            print("Now you can login")
    else:
        # with open(f"{username}.json", "r") as person:
        #     file1 = json.load(person)
        print('User exists')
    # return file1


def logout():

    try:
        username = input("Please enter Username you want to logout: ")
        if os.path.exists(f"{os.getcwd()}/{username}.json") or os.path.exists(f'{username}.pickle'):
            os.remove(f'{username}.pickle')
            os.remove(f'{username}.json')
            os.remove(f'student.json')
            os.remove(f'clinix.json')
            os.remove(f'combined_calendar_list.json')
            os.remove(f'{os.getcwd()}/TempData/temp.txt')
            print(f'{username} successfully removed from system')
        else:
            print('No user found')
    except Exception as error:
        print('Error:', error)


def password_hasher(pword1, pword2):
    """
    This function will encrypt the password
    """
    # salt = uuid.uuid4().hex
    return hashlib.sha512(pword1.encode('utf-8')).hexdigest()


def password_validator(pword1, file1):
    """
    This funtion vaildates the password
    """
    input_pass = password_hasher(pword1, pword1)
    return input_pass == file1


def password_hasher(pword1, pword2):
    """
    This function will encrypt the password
    """
    # salt = uuid.uuid4().hex
    return hashlib.sha512(pword1.encode('utf-8')).hexdigest()


"TODO check pickle's expiry"


def get_user_info():
    """

    """
    global is_logged_in
    # global username
    username = input("Please enter student username: ")
    if os.path.exists(f"{username}.json"):
        with open(f"{username}.json", "r") as person:
            person_info = json.loads(person.read())
            # print("Please enter password to login ")
            if password_validator(stdiomask.getpass("Please enter password to login: "), person_info["password"]):
                is_logged_in = True
                create_temp_data(username)
                if os.path.exists(f'{username}.pickle'):
                    return True, person_info
                else:
                    return True, person_info
            else:
                print("Incorrect password")
                exit()
                # return False, "Incorrect password"
    else:
        print("Use 'clinix init'")
        exit()
# print(create_profile())

def create_temp_data(username):
    """
    Creates a temporary data file which stores the username of the person logged in
    """
    if os.path.exists(os.getcwd()+"/TempData/temp.txt"):
        with open(os.getcwd()+'/TempData/temp.txt', 'r') as temp_file:
            print("Welcome back,", temp_file.read())
    else:
        with open(os.getcwd()+'/TempData/temp.txt', 'w') as temp_file:
            temp_file.write(username)

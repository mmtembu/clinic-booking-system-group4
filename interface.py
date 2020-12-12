import sys
import json
import os
import stdiomask
import hashlib
import uuid
import tempfile


"""
Interface Module handles user profiles and handles login details
"""


is_logged_in = False


def create_profile():
    """
    This funtion creates the users config file if one doesnt exist and
    file path if one exist
    """

    file1 = None
    username = input("Please enter student username: ")
    if not os.path.exists(f"{os.getcwd()}/{username}.json"):
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
        print('User exists')


def logout():
    """
    Logout deletes all user related info/files
    """

    try:
        username = input("Please enter Username you want to logout: ")
        if os.path.exists(f"{os.getcwd()}/{username}.json") or os.path.exists(f'{username}.pickle'):
            if os.path.exists((f'{username}.pickle')):
                os.remove(f'{username}.pickle')
            if os.path.exists((f'{username}.json')):
                os.remove(f'{username}.json')
            if os.path.exists(f'student.json'):
                os.remove(f'student.json')
            if os.path.exists(f'clinix.json'):
                os.remove(f'clinix.json')
            if os.path.exists(f'combined_calendar_list.json'):
                os.remove(f'combined_calendar_list.json')
            if os.path.exists(f'{os.getcwd()}/TempData/temp.txt'):
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


def get_user_info():
    """
    Handles the login and validates the password and user
    """
    global is_logged_in
    username = input("Please enter student username: ")
    if os.path.exists(f"{username}.json"):
        with open(f"{username}.json", "r") as person:
            person_info = json.loads(person.read())
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
    else:
        print("Use 'clinix init'")
        exit()


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

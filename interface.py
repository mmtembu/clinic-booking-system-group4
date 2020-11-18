import sys
import json
import os
import stdiomask
import hashlib
import uuid

# username = ''
is_logged_in = False

"""
TODO: Don't forget to account for empty strings when creating a json file
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
        pword1 = stdiomask.getpass("Please enter password: ")
        pword2 = stdiomask.getpass("Please confirm password: ")

        while pword1 != pword2:
            print("Password doesn't match : ")
            pword1 = stdiomask.getpass("Please enter password: ")
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
            os.remove(f'student.csv')
            os.remove(f'clinix.csv')
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
                if os.path.exists(f'{username}.pickle'):
                    # print("Token expiry: ")
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

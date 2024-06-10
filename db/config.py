import flet as ft
from flet import *
import pyrebase
import requests
import json
from flet_route import Params, Basket, params
from flet_core.control_event import ControlEvent

username = None

firebaseConfig = {
    "apiKey": "AIzaSyDvZsBy92nHhTwkqOOQ4tEt9yocgYd77zM",
    "authDomain": "calladoctor-605b5.firebaseapp.com",
    "databaseURL": "https://calladoctor-605b5-default-rtdb.firebaseio.com",
    "projectId": "calladoctor-605b5",
    "storageBucket": "calladoctor-605b5.appspot.com",
    "messagingSenderId": "931118860774",
    "appId": "1:931118860774:web:7a27610ad6ef55debe2e27"
}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

def register(email, password, name):
    try:
        user = auth.create_user_with_email_and_password(email, password)

        url = "http://localhost:3000/user"

        userID = user['localId']

        payload = f'userID={userID}&name={name}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    except:
        print("Email already exists")
    return

def login(email, password):
    global username
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        userID = auth.get_account_info(login['idToken'])['users'][0]['localId']

        url = f"http://localhost:3000/username/{userID}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        username = json.loads(response.text)['name']

        return True
    except:
        print("Invalid email or password")
    return

def get_name():
    return username
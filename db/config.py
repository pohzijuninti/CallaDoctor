import flet as ft
from flet import *
import pyrebase
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent

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

def register(email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
    except:
        print("Email already exists")
    return

def login(email, password):
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print(auth.get_account_info(login['idToken'])['users'][0]['localId'])
        return True
    except:
        print("Invalid email or password")
    return
import pyrebase
import requests
import json


# Initialize global variables for username and userID
username = None
userID = None

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyDvZsBy92nHhTwkqOOQ4tEt9yocgYd77zM",
    "authDomain": "calladoctor-605b5.firebaseapp.com",
    "databaseURL": "https://calladoctor-605b5-default-rtdb.firebaseio.com",
    "projectId": "calladoctor-605b5",
    "storageBucket": "calladoctor-605b5.appspot.com",
    "messagingSenderId": "931118860774",
    "appId": "1:931118860774:web:7a27610ad6ef55debe2e27"
}

# Initialize Firebase app with the provided configuration
firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()


# Function to register a new user
def register(email, password, name, ic):
    try:
        # Create a new user with email and password
        user = auth.create_user_with_email_and_password(email, password)

        # Define the API endpoint for user registration
        url = "http://localhost:3000/user"

        # Extract the userID from the created user
        userID = user['localId']

        # Prepare the payload with user details
        payload = f'userID={userID}&name={name}&ic={ic}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        # Send a POST request to register the user in the backend
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
    except:  # Handle the case where the email already exists
        print("Email already exists")
    return


# Function to login a user
def login(email, password):
    global username
    global userID

    try:
        # Sign in the user with email and password
        login = auth.sign_in_with_email_and_password(email, password)

        # Get the userID from the login response
        userID = auth.get_account_info(login['idToken'])['users'][0]['localId']

        # Define the API endpoint to get user details
        url = f"http://localhost:3000/user/{userID}"

        payload = {}
        headers = {}

        # Send a GET request to fetch user details
        response = requests.request("GET", url, headers=headers, data=payload)

        # Extract the username from the response
        username = json.loads(response.text)['name']

        return True
    except:  # Handle login failure
        return False


# Function to get the username
def get_name():
    return username


# Function to get the userID
def get_userID():
    return userID
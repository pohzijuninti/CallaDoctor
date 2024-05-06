import pyrebase

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

def Signup(email, password):
    # email = input("Enter email: ")
    # password = input("Enter password: ")
    user = auth.create_user_with_email_and_password(email, password)

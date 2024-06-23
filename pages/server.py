import requests
import datetime

# Initialize lists to store data fetched from server
hospitalList = []
doctorList = []
specialityList = []
doctorFilteredList = []

# URL of the server.js endpoint
url = 'http://localhost:3000/'

payload = {}
headers = {}

# Fetch hospital data from server
response = requests.request("GET", url + 'hospital', headers=headers, data=payload)
if response.status_code == 200:
    hospitalList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)

# Fetch doctor data from server
response = requests.request("GET", url + 'doctor', headers=headers, data=payload)
if response.status_code == 200:
    doctorList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)

# Fetch speciality data from server
response = requests.request("GET", url + 'speciality', headers=headers, data=payload)
if response.status_code == 200:
    specialityList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)


# Function to get time slot for a hospital based on hospital ID
def get_time_slot(hospital_id):
    for hospital in hospitalList:
        if hospital['hospitalID'] == hospital_id:
            return hospital['name']
    return None


# Function to get hospital name based on hospital ID
def get_hospital_name(hospital_id):
    for hospital in hospitalList:
        if hospital['hospitalID'] == hospital_id:
            return hospital['name']
    return None


# Function to get list of doctors filtered by hospital ID
def get_doctor_details(hospital_id):
    global doctorFilteredList
    doctorFilteredList = []
    for doctor in doctorList:
        if doctor['hospitalID'] == hospital_id:
            doctorFilteredList.append(doctor)
    return None


# Function to get doctor name based on doctor ID
def get_doctor_name(doctor_id):
    for doctor in doctorList:
        if doctor['doctorID'] == doctor_id:
            return doctor['name']
    return None


# Function to get speciality name based on speciality ID
def get_speciality_name(specialty_id):
    for speciality in specialityList:
        if speciality['specialityID'] == specialty_id:
            return speciality['name']
    return None


# Function to convert timestamp to formatted date
def convert_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d %B %Y")


# Function to convert timestamp to formatted time (12-hour clock format)
def convert_time(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%I:%M %p")
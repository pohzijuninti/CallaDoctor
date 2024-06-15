import requests
import datetime

hospitalList = []
doctorList = []
specialityList = []
doctorFilteredList = []
descriptionList = []

# URL of the server.js endpoint
url = 'http://localhost:3000/'

payload = {}
headers = {}

# Hospital
response = requests.request("GET", url + 'hospital', headers=headers, data=payload)
if response.status_code == 200:
    hospitalList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)

# Doctor
response = requests.request("GET", url + 'doctor', headers=headers, data=payload)
if response.status_code == 200:
    doctorList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)

# Speciality
response = requests.request("GET", url + 'speciality', headers=headers, data=payload)
if response.status_code == 200:
    specialityList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)

# Description
response = requests.request("GET", url + 'description', headers=headers, data=payload)
if response.status_code == 200:
    descriptionList = response.json()  # Assuming the server.js endpoint returns JSON data
else:
    print('Error:', response.status_code)


def get_time_slot(hospital_id):
    for hospital in hospitalList:
        if hospital['hospitalID'] == hospital_id:
            return hospital['name']
    return None


def get_hospital_name(hospital_id):
    for hospital in hospitalList:
        if hospital['hospitalID'] == hospital_id:
            return hospital['name']
    return None


def get_doctor_details(hospital_id):
    global doctorFilteredList
    doctorFilteredList = []
    for doctor in doctorList:
        if doctor['hospitalID'] == hospital_id:
            doctorFilteredList.append(doctor)
    return None


def get_doctor_name(doctor_id):
    for doctor in doctorList:
        if doctor['doctorID'] == doctor_id:
            return doctor['name']
    return None


def get_speciality_name(specialty_id):
    for speciality in specialityList:
        if speciality['specialityID'] == specialty_id:
            return speciality['name']
    return None


def convert_date(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%d %B %Y")


def convert_time(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%I:%M %p")
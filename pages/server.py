import requests
from db.config import get_userID

hospitalList = []
doctorList = []
specialityList = []
doctorFilteredList = []
descriptionList = []
appointments = []

# URL of the server.js endpoint
url = 'http://localhost:3000/'

# Send a GET request to the server.js endpoint
hospital_response = requests.get(url + 'hospital')
# Check if the request was successful (status code 200)
if hospital_response.status_code == 200:
    # Access the response data
    data = hospital_response.json()  # Assuming the server.js endpoint returns JSON data
    hospitalList = data
else:
    print('Error:', hospital_response.status_code)


doctor_response = requests.get(url + 'doctor')
if doctor_response.status_code == 200:
    data = doctor_response.json()
    doctorList = data
else:
    print('Error:', doctor_response.status_code)


speciality_response = requests.get(url + 'speciality')
if speciality_response.status_code == 200:
    data = speciality_response.json()
    specialityList = data
else:
    print('Error:', speciality_response.status_code)


description_response = requests.get(url + 'description')
if description_response.status_code == 200:
    data = description_response.json()
    descriptionList = data
else:
    print('Error:', description_response.status_code)


def get_appointments(user_id):
    global appointments
    appointments = []

    appointment_response = requests.get(url + f'appointment/:{user_id}')
    if appointment_response.status_code == 200:
        appointments = appointment_response.json()
        print(appointments)
    else:
        print('Error:', appointment_response.status_code)


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
    for doctor in doctorFilteredList:
        if doctor['doctorID'] == doctor_id:
            return doctor['name']
    return None


def get_speciality_name(specialty_id):
    for speciality in specialityList:
        if speciality['specialityID'] == specialty_id:
            return speciality['name']
    return None




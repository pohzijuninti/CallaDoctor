import requests

hospitalList = []
doctorList = []
specialityList = []
doctorFilteredList = []

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

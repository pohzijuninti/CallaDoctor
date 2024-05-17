import requests

hospitalList = []
doctorList = []
specialityList = []

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


def get_specialty_name(specialty_id):
    for specialty in specialityList:
        if specialty['specialityID'] == specialty_id:
            return specialty['name']
    return None

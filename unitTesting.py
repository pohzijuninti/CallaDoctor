import unittest
from unittest.mock import patch, Mock
import json

# Import functions and classes to test
from db.config import get_userID, login
from pages.home import Home
from pages.medicalRecord import MedicalRecord
from pages.patientList import PatientList


class UnitTesting(unittest.TestCase):

    def setUp(self):
        # Setup that will be run before each test case
        self.patcher1 = patch('db.config.userID', 'mock_user_id')
        self.mock_userID = self.patcher1.start()

    def tearDown(self):
        # Cleanup that will be run after each test case
        self.patcher1.stop()

    def test_get_userID(self):
        # Test case for get_userID function
        self.assertEqual(get_userID(), "mock_user_id")

    @patch('db.config.auth.sign_in_with_email_and_password')
    def test_failed_login(self, mock_sign_in):
        # Mock the response of sign_in_with_email_and_password to simulate failure
        mock_sign_in.side_effect = Exception("Authentication failed")

        # Call the login function with mock credentials
        result = login('test@example.com', 'password')

        # Assertions
        self.assertFalse(result)  # Ensure login failed
        self.assertEqual(mock_sign_in.call_count, 1)  # Verify sign_in_with_email_and_password was called

    @patch('requests.get')
    def test_get_appointments(self, mock_get):
        # Create a mock response object with the desired JSON data
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"bookID": 10001, "userID": "Ab1C23", "datetime": 1719115200, "status": 0, "hospitalID": 1, "doctorID": 21},
            {"bookID": 10002, "userID": "De4F56", "datetime": 1719118800, "status": 1, "hospitalID": 2, "doctorID": 22}
        ])
        mock_get.return_value = mock_response

        # Create an instance of the Home class
        home = Home()

        # Call the get_appointments method
        home.get_appointments()

        # Verify that the appointments attribute was set correctly
        self.assertEqual(len(home.appointments), 2)
        self.assertEqual(home.appointments[0]["bookID"], 10001)
        self.assertEqual(home.appointments[1]["userID"], "De4F56")

        # Verify that the requests.get method was called with the correct URL
        mock_get.assert_called_once_with(
            f'http://localhost:3000/appointment/{get_userID()}',
            headers=home.headers,
            data=home.payload
        )

    @patch('requests.get')
    def test_get_medical_records(self, mock_get):
        # Create a mock response object with the desired JSON data
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"recordID": 201, "datetime": 1717830000, "title": "Broke His Left Leg", "description": "Fall down from bicycle , Broke his left leg", "hospitalID": 5, "doctorID": 35, "userID": "Ab1C23"},
            {"recordID": 203, "datetime": 1718445600, "title": "Pulmonary Edema", "description": "Difficult to breathe", "hospitalID": 5, "doctorID": 35, "userID": "De4F56"}
        ])
        mock_get.return_value = mock_response

        # Create an instance of the MedicalRecord class
        medical_record = MedicalRecord()

        # Call the get_medical_records method
        medical_record.get_medical_records()

        # Verify that the medical_record attribute was set correctly
        self.assertEqual(len(medical_record.medical_record), 2)
        self.assertEqual(medical_record.medical_record[0]["recordID"], 201)
        self.assertEqual(medical_record.medical_record[1]["title"], "Pulmonary Edema")

        # Verify that the requests.get method was called with the correct URL
        mock_get.assert_called_once_with(
            f"http://localhost:3000/medicalRecord/{get_userID()}",
            headers=medical_record.headers,
            data=medical_record.payload
        )

    @patch('requests.get')
    def test_get_users(self, mock_get):
        # Create a mock response object with desired JSON data
        mock_response = Mock()
        mock_response.text = json.dumps([
            {"userID": "Gh7I89", "name": "Poh"},
            {"userID": "Jk1L23", "name": "Pooh"}
        ])
        mock_get.return_value = mock_response

        # Create an instance of the PatientList class
        patient_list = PatientList()

        # Call the get_users method
        patient_list.get_users()

        # Assert that the patient_list attribute is correctly populated
        self.assertEqual(len(patient_list.patients), 2)
        self.assertEqual(patient_list.patients[0]["userID"], "Gh7I89")
        self.assertEqual(patient_list.patients[1]["name"], "Pooh")

        # Verify that the requests.get method was called with the correct URL
        mock_get.assert_called_once_with(
            "http://localhost:3000/user/get",
            headers=patient_list.headers,
            data=patient_list.payload
        )


if __name__ == '__main__':
    unittest.main()


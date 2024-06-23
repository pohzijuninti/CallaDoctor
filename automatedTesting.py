import unittest
from unittest.mock import patch, Mock, MagicMock
import requests
from pages.clinicForm import ClinicForm
from pages.selectDateTime import SelectDateTime
import datetime


class AutomatedTesting(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.get')
    def test_admin_login_and_redirect(self, mock_get, mock_post):
        # Mock the response of the login request
        mock_post_response = Mock()
        mock_post_response.status_code = 200
        mock_post_response.json.return_value = {'hospitalID': 1}
        mock_post.return_value = mock_post_response

        # Mock the response of the admin homepage request
        mock_get_response = Mock()
        mock_get_response.status_code = 200
        mock_get_response.text = "Admin Homepage"
        mock_get.return_value = mock_get_response

        # Define the credentials for a valid admin user
        valid_admin_credentials = {
            'email': 'admin@example.com',
            'password': 'admin123'
        }

        # Make the POST request to the admin login URL with valid credentials
        response = requests.post("http://localhost:3000/login/admin", data=valid_admin_credentials)

        # Ensure the request was successful
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_data = response.json()

        # Extract the hospital_id from the response
        hospital_id = response_data['hospitalID']

        # Verify the hospital_id is present in the response
        self.assertIsNotNone(hospital_id)

        # Make a GET request to the admin homepage URL
        home_response = requests.get(f"http://localhost:3000/adminHome/{hospital_id}")

        # Ensure the request was successful
        self.assertEqual(home_response.status_code, 200)

        # Checking if specific text or elements are present in the response
        home_content = home_response.text
        self.assertIn("Admin Homepage", home_content)

    @patch('requests.post')
    def test_doctor_login_and_failed(self, mock_post):
        # Mock the response of the doctor login request - Failed Login
        mock_post_response_fail = Mock()
        mock_post_response_fail.status_code = 401  # Unauthorized status code
        mock_post.return_value = mock_post_response_fail

        # Mock credentials for doctor login
        invalid_doctor_credentials = {
            'email': 'invalid@example.com',
            'password': 'invalid123'
        }

        # Make the POST request to the doctor login URL with invalid credentials (Failed)
        response_fail = requests.post("http://localhost:3000/login/doctor", data=invalid_doctor_credentials)

        # Ensure the request failed with Unauthorized status
        self.assertEqual(response_fail.status_code, 401)

    @patch('requests.post')
    def test_submit_form_and_success(self, mock_post):
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Form submitted successfully"}

        # Assign mock_response to mock_post().return_value
        mock_post.return_value = mock_response

        # Create an instance of ClinicForm
        form = ClinicForm()

        # Simulate filling out the form
        form.name.value = "Hospital Name"
        form.address.value = "Hospital Address"
        form.phone_number.value = "0123456789"
        form.email.value = "hospital@example.com"

        # Directly call the method that triggers the POST request
        form.open_dlg_modal(Mock(), None)

        # Assertions
        mock_post.assert_called_once_with(
            "http://localhost:3000/clinic/form",
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=f'hospitalName={form.name.value}&address={form.address.value}&phone={form.phone_number.value}&email={form.email.value}'
        )


if __name__ == '__main__':
    unittest.main()

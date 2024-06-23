import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json


class DoctorInfo():
    def __init__(self):
        self.doctor_info = None
        self.hospital_name = None
        self.speciality_name = None

    # Fetches doctor info for the specified doctor ID
    def get_doctor_info(self, doctor_id):
        url = f"http://localhost:3000/doctor/get/{doctor_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.doctor_info = json.loads(response.text)
        print(self.doctor_info)

    # Fetches hospital name for the specified doctor ID
    def get_hospital_name(self, doctor_id):
        url = f"http://localhost:3000/hospital/name/{doctor_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.hospital_name = json.loads(response.text)['name']

    # Fetches speciality name for the specified speciality ID
    def get_speciality(self, speciality_id):
        url = f"http://localhost:3000/speciality/{speciality_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.speciality_name = json.loads(response.text)['name']

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        doctor_id = int(params.doctor_id)
        self.get_doctor_info(doctor_id)
        self.get_hospital_name(self.doctor_info['hospitalID'])
        self.get_speciality(self.doctor_info['specialityID'])

        title = self.doctor_info['name'] + ' - ' + self.hospital_name
        page.title = title
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        # Navigate to select doctor page
        def go_select_doctor(e):
            hospital_id = self.doctor_info['hospitalID']
            page.go(f'/selectDoctor/{hospital_id}')
            page.update()

        email = self.doctor_info['email']

        return View(
            bgcolor=colors.GREY_200,
            route="/doctor/info/:doctor_id",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    controls=[
                        IconButton(
                            icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                            icon_color=colors.GREY_800,
                            on_click=go_select_doctor,
                        ),
                        Row(
                            controls=[
                                Container(
                                    height=300,
                                    width=300,
                                    content=Image(src=self.doctor_info['image']),
                                ),
                                Container(
                                    padding=10,
                                    content=Row(
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Column(
                                                controls=[
                                                    Text('Name: '),
                                                    Text('Hospital: '),
                                                    Text('Speciality: '),
                                                    Text('Email: '),
                                                ]
                                            ),
                                            Column(
                                                controls=[
                                                    Text(self.doctor_info['name']),
                                                    Text(self.hospital_name),
                                                    Text(self.speciality_name),
                                                    Text(email)
                                                ]
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )

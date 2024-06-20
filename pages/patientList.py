import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json

class PatientList:
    def __init__(self):
        self.headers = {}
        self.payload = {}
        self.response = None
        self.patients = None
        self.hospital_id = None

    def get_users(self):
        full_url = "http://localhost:3000/user/get"
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        self.patients = json.loads(self.response.text)

    def get_hospital_id(self, docID):
        url = f"http://localhost:3000/doctor/get/{docID}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        self.hospital_id = json.loads(response.text)['hospitalID']


    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Doctor - Patient List'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        doctor_id = int(params.doctor_id)

        self.get_users()
        self.get_hospital_id(doctor_id)


        def go_doctor_home(e):
            page.go(f'/doctorHome/{doctor_id}')
            page.update()

        def go_doctor_medical_record(hospital_id, user_id):
            page.go(f"/doctorMedicalRecord2/{hospital_id}/{doctor_id}/{user_id}")
            page.update()

        patients = ListView(
            expand=True,
            spacing=10,
            padding=20,
        )

        def update_patient_view():
            patients.controls.clear()

            for i in range(len(self.patients)):
                name = self.patients[i]['name']
                ic = self.patients[i]['ic']
                patients.controls.append(
                    ListTile(
                        shape=RoundedRectangleBorder(
                            radius=10
                        ),
                        bgcolor='white',
                        leading=Icon(icons.PERSON, size=30),
                        title=Text(name),
                        subtitle=Text(ic),
                        trailing=IconButton(
                            data=self.patients[i]['userID'],
                            icon=icons.EDIT_DOCUMENT,
                            on_click=lambda e: go_doctor_medical_record(self.hospital_id, e.control.data)
                        )
                    ),
                )

        update_patient_view()

        return View(
            padding=50,
            spacing=50,
            bgcolor=colors.GREY_200,
            route="/doctor/patientList/:hospital_id/:doctor_id",
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.GREY_800,
                                    on_click=go_doctor_home,
                                ),
                                Text(
                                    value='Patient List',
                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=patients
                        ),
                    ]
                )
            ]
        )
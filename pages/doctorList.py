import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import ast

class DoctorList:
    def __init__(self):
        self.doctors = None

    def get_doctors(self):
        url = "http://localhost:3000/doctor"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        self.doctors = json.loads(response.text)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Doctor List'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        self.get_doctors()

        medical_record = ast.literal_eval(params.medicalRecord)

        def go_medical_record(e):
            page.go("/medicalRecord")
            page.update()

        def send_medical_record(e, docID):
            print(docID)
            recordID = medical_record['recordID']
            datetime1 = medical_record['datetime']
            title = medical_record['title']
            description = medical_record['description']
            hospital_id = medical_record['hospitalID']
            doctor_id = medical_record['doctorID']
            user_id = medical_record['userID']

            url = "http://localhost:3000/share/medicalRecord"

            payload = f'recordID={recordID}&datetime={datetime1}&title={title}&description={description}&hospitalID={hospital_id}&doctorID={doctor_id}&userID={user_id}&sharedDoctorID={docID}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            dlg_modal.open = False
            page.update()

        def handle_close(e):
            dlg_modal.open = False
            page.update()

        def open_dlg_modal(e):
            dlg_modal.content = Text(f"Do you really want to send the medical record to {e.control.data['name']}?")
            page.dialog = dlg_modal
            dlg_modal.data = e.control.data['doctorID']
            dlg_modal.open = True
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text(""),
            actions=[
                ft.TextButton(text="Yes", on_click=lambda e: send_medical_record(e, dlg_modal.data)),
                ft.TextButton(text="No", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )

        doctors = ListView(
            expand=True,
            spacing=10,
            padding=20,
        )

        for i in range(len(self.doctors)):
            name = self.doctors[i]['name']
            hospitalID = self.doctors[i]['hospitalID']

            url = f"http://localhost:3000/hospital/name/{hospitalID}"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            hospital = json.loads(response.text)['name']

            doctors.controls.append(
                ListTile(
                    on_click=open_dlg_modal,
                    shape=RoundedRectangleBorder(
                        radius=10
                    ),
                    bgcolor='white',
                    data=self.doctors[i],
                    leading=Icon(icons.PERSON, size=30),
                    title=Text(name),
                    subtitle=Text(hospital),
                )
            )

        return View(
            padding=50,
            spacing=50,
            bgcolor=colors.GREY_200,
            route="/doctorList/:medicalRecord",
            controls=[
                Column(
                    expand=True,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.GREY_800,
                                    on_click=go_medical_record,
                                ),
                                Text(
                                    value='Doctor List',
                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=doctors
                        ),
                    ]
                )
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
import datetime
import requests
import json
from db.config import get_name, get_userID
import pages.server as svr


class MedicalRecord:
    def __init__(self):
        self.url = "http://localhost:3000/medicalRecord"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.medical_record = None

    def get_medical_records(self):
        full_url = f"{self.url}/{get_userID()}"
        print(full_url)
        # Perform the HTTP request to fetch appointments
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        # Store the response text data
        self.medical_record = json.loads(self.response.text)
        print(self.medical_record)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        self.get_medical_records()

        def go_home(e):
            page.go("/home")
            page.update()

        def name_card():
            gender = 'Male'
            age = '24 years old'
            caution = 'Allergic to Panadol'
            return Container(
                width=300,
                height=150,
                border_radius=10,
                bgcolor="white",
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Icon(icons.PERSON,
                                             color=colors.BLACK,
                                             size=50,
                                             ),
                                    ]
                                ),
                                Column(
                                    expand=2,
                                    controls=[
                                        Text(value=f"{get_name()}\n{gender}\n{age}", style=TextStyle(color=colors.BLACK)),
                                        Text(value=f"**{caution}**", style=TextStyle(color=colors.RED)),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            )

        def display_description(description):
            if ',' in description:
                description = description.replace(',', '\n*')
            if not description.startswith('*'):
                description = '* ' + description
            return description

        medical_records = GridView(
            runs_count=3,
            child_aspect_ratio=10 / 9,
        )

        for i in range(len(self.medical_record)):
            medical_records.controls.append(
                Container(
                    border_radius=10,
                    bgcolor='white',
                    content=Container(
                        padding=10,
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Column(
                                    controls=[
                                        Text(value=f'{svr.convert_date(self.medical_record[i]["datetime"])}, {svr.convert_time(self.medical_record[i]["datetime"])}', color=colors.GREY),
                                        Text(value=f'{self.medical_record[i]["title"]}', size=18, color=colors.BLACK,
                                             weight=FontWeight.BOLD),
                                        Text(value='Description', color=colors.BLACK),
                                        Text(value=f'{display_description(self.medical_record[i]["description"])}', color=colors.GREY),
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        Text(value=f'{svr.get_hospital_name(self.medical_record[i]["hospitalID"])}, {svr.get_doctor_name(self.medical_record[i]["doctorID"])}', color=colors.BLACK, size=12),
                                        IconButton(icon=icons.SEND, icon_color=colors.BLUE),
                                    ]
                                )

                            ]
                        )
                    )
                )
            )

        return View(
            route="/medicalRecord",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.WHITE,
                                    on_click=go_home,
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        name_card(),
                        Container(
                            expand=True,
                            content=medical_records,
                        ),
                    ]
                ),
            ]
        )

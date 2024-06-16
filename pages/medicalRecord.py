import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
from db.config import get_name, get_userID
import pages.server as svr
import datetime


class MedicalRecord:
    def __init__(self):
        self.medical_record_url = "http://localhost:3000/medicalRecord"
        self.name_card_url ="http://localhost:3000/username"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response1 = None
        self.response2 = None
        self.medical_record = None
        self.name_card = None

    def get_name_card(self):
        full_url = f'{self.name_card_url}/{get_userID()}'
        self.response1 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.name_card = json.loads(self.response1.text)


    def get_medical_records(self):
        full_url = f"{self.medical_record_url}/{get_userID()}"
        self.response2 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.medical_record = json.loads(self.response2.text)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        self.get_medical_records()
        self.get_name_card()

        def go_home(e):
            page.go("/home")
            page.update()

        def name_card():
            is_odd = int(self.name_card['ic'][-1]) % 2 != 0
            if is_odd:
                gender = "Male"
            else:
                gender = "Female"

            current_date = datetime.datetime.now()

            current_year_two_digit = int(str(current_date.year)[-2:])
            current_year = int(str(current_date.year))
            ic_year = int(self.name_card['ic'][:2])

            if ic_year <= current_year_two_digit:
                birth_year = 2000 + ic_year
            else:
                birth_year = 1900 + ic_year

            age = str(current_year - birth_year) + ' years old'
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
                                        Text(value=f'{svr.get_hospital_name(self.medical_record[i]["hospitalID"])}\n{svr.get_doctor_name(self.medical_record[i]["doctorID"])}', color=colors.BLACK, size=12),
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

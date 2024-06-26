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
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response1 = None
        self.response2 = None
        self.medical_record = None
        self.name_card = None

    # Fetch user's name card data from server based on user ID
    def get_name_card(self):
        full_url = f'http://localhost:3000/user/{get_userID()}'
        self.response1 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.name_card = json.loads(self.response1.text)

    # Fetch medical records of the current user from server based on user ID
    def get_medical_records(self):
        full_url = f"http://localhost:3000/medicalRecord/{get_userID()}"
        self.response2 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.medical_record = json.loads(self.response2.text)

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        self.get_medical_records()
        self.get_name_card()

        # Navigate to home page
        def go_home(e):
            page.go("/home")
            page.update()

        # Navigate to doctor list page with selected medical record
        def send_medical_record(e):
            page.go(f'/doctorList/{e.control.data}')
            page.update()

        # Generate user's name card based on fetched data
        def name_card():
            # Determine gender based on the last digit of IC number
            ic_number = self.name_card['ic']

            # Extract digits from ic_number
            digits = ''.join(c for c in ic_number if c.isdigit())

            # Take the first 12 digits
            ic_digits = digits[:12]

            is_odd = int(ic_digits[-1]) % 2 != 0
            gender = "Male" if is_odd else "Female"

            # Calculate user's age based on IC birth year
            current_date = datetime.datetime.now()
            current_year = current_date.year
            ic_year = int(ic_digits[:2])
            current_year_two_digit = int(str(current_year)[-2:])
            birth_year = 2000 + ic_year if ic_year <= current_year_two_digit else 1900 + ic_year
            age = f"{current_year - birth_year} years old"

            # Display caution message if available
            caution = self.name_card['caution']
            caution_text = Text(value=f'{caution}', style=TextStyle(color=colors.RED)) if caution else None

            content_controls = [
                Row(
                    controls=[
                        Column(
                            expand=1,
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Icon(icons.PERSON, color=colors.BLACK, size=50),
                            ]
                        ),
                        Column(
                            expand=2,
                            controls=[
                                Text(value=f"{get_name()}\n{gender}\n{age}", style=TextStyle(color=colors.BLACK)),
                            ]
                        ),
                    ]
                ),
            ]

            # Add caution text if available
            if caution_text:
                content_controls[0].controls[1].controls.append(caution_text)

            return Container(
                width=300,
                height=150,
                border_radius=10,
                bgcolor="white",
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=content_controls
                )
            )

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
                                        Text(value=f'{self.medical_record[i]["title"]}', size=18, color=colors.BLACK, weight=FontWeight.BOLD),
                                        Text(value='Description', color=colors.BLACK),
                                        Text(value=f'{self.medical_record[i]["description"]}', color=colors.GREY),
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        Text(value=f'{svr.get_hospital_name(self.medical_record[i]["hospitalID"])}\n{svr.get_doctor_name(self.medical_record[i]["doctorID"])}', color=colors.BLACK, size=12),
                                        IconButton(icon=icons.SEND, data=self.medical_record[i], icon_color=colors.BLUE, on_click=lambda e: send_medical_record(e))
                                    ]
                                )

                            ]
                        )
                    )
                )
            )

        return View(
            bgcolor=colors.GREY_200,
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
                                    icon_color=colors.BLACK,
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

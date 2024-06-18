import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import time
import datetime
import pages.server as svr

from pages.doctorHome import doctor_id

class DoctorMedicalRecord:

    def __init__(self):
        self.name_card_url = "http://localhost:3000/username"
        self.medical_record_url = "http://localhost:3000/medicalRecord"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response1 = None
        self.response2 = None
        self.name_card = None
        self.medical_record = None


    def get_name_card(self, user_id):
        full_url = f'{self.name_card_url}/{user_id}'
        self.response1 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.name_card = json.loads(self.response1.text)

    def get_medical_records(self, user_id):
        full_url = f"{self.medical_record_url}/{user_id}"
        self.response2 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.medical_record = json.loads(self.response2.text)


    def view(self, page: Page, params: Params, basket: Basket):
        patientName = None
        page.title = f'{patientName} - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        user_id = params.user_id
        doctor_id = int(params.doctor_id)
        #
        print(doctor_id)

        self.get_name_card(user_id)
        self.get_medical_records(user_id)

        # def go_doctor_home():
        #     page.go(f'/doctorHome/{doctor_id}')
        #     page.update()

        title: TextField = TextField(label='Title', width=250, border=InputBorder.UNDERLINE, text_size=14)
        description: TextField = TextField(label='Description', width=250, border=InputBorder.UNDERLINE, text_size=14,
                                           multiline=True, min_lines=3, max_lines=3)

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def close_dlg(e):
            current_unix_time = int(time.time())
            url = "http://localhost:3000/medicalRecord/add"

            payload = f'datetime={current_unix_time}&title={title.value}&description={description.value}&hospitalID={5}&doctorID={35}&userID={user_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            dlg_modal.open = False
            title.value = ''
            description.value = ''
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Medical Record"),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            title,
                            description,
                            Container(padding=padding.only(top=20, bottom=10),
                                      content=ElevatedButton(text="Done",
                                                             on_click=close_dlg,
                                                             width=250))]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

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
                                        Text(value=f"{self.name_card['name']}\n{self.name_card['ic']}\n{gender}\n{age}", style=TextStyle(color=colors.BLACK)),
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
                                    ]
                                )

                            ]
                        )
                    )
                )
            )

        return View(
            route="/doctor/medicalRecord/:doctor_id:user_id",
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
                                    # on_click=go_doctor_home,
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                name_card(),
                                ElevatedButton(
                                    on_click=open_dlg_modal,
                                    content=Text('Add Medical Record')
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            content=medical_records,
                        ),
                    ]
                ),
            ]
        )
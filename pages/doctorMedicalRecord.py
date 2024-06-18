import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import datetime

class DoctorMedicalRecord:

    def __init__(self):
        self.name_card_url = "http://localhost:3000/username"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response1 = None
        self.name_card = None



    def get_name_card(self, user_id):
        full_url = f'{self.name_card_url}/{user_id}'
        self.response1 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.name_card = json.loads(self.response1.text)

        print(self.name_card)

    def view(self, page: Page, params: Params, basket: Basket):
        patientName = None
        page.title = f'{patientName} - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        user_id = params.user_id

        print(user_id)

        self.get_name_card(user_id)


        return View(
            route="/doctor/medicalRecord/:user_id",
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
                                    # on_click=go_home,
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        # name_card(),
                        # Container(
                        #     expand=True,
                        #     content=medical_records,
                        # ),
                    ]
                ),
            ]
        )

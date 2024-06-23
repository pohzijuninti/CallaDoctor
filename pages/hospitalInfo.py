import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json


class HospitalInfo():
    def __init__(self):
        self.hospital = None

    # Fetches hospital info for the specified hospital ID
    def get_hospital_info(self, hospital_id):
        url = f"http://localhost:3000/hospital/{hospital_id}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        self.hospital = json.loads(response.text)

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        hospital_id = int(params.hospital_id)
        self.get_hospital_info(hospital_id)
        hospital_name = self.hospital['name']

        page.title = hospital_name
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        # Navigate to select hospital page
        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

        return View(
            bgcolor=colors.GREY_200,
            route="/hospital/info/:hospital_id",
            padding=50,
            spacing=50,
            controls=[
                ListView(
                    expand=True,
                    controls=[
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.GREY_800,
                                    on_click=go_select_hospital,
                                ),
                                Text(
                                    value=hospital_name,
                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                ),
                                Container()
                            ]
                        ),
                        Container(
                            padding=10,
                            content=Image(
                                width=300,
                                height=300,
                                src=self.hospital['image'],
                                fit=ImageFit.FILL,
                            ),
                        ),
                        Container(
                            padding=10,
                            content=Text('Location: ' + self.hospital['location'])
                        ),
                        Container(
                            padding=10,
                            content=Image(
                                height=200,
                                width=500,
                                src=self.hospital['map'],
                                fit=ImageFit.COVER,
                            ),
                        ),
                        Container(
                            padding=10,
                            content=Text(self.hospital['description'])
                        ),
                    ]
                )
            ]
        )
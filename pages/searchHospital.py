import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json

class SearchHospital:
    def __init__(self):
        self.hospitals = None
        self.url = "http://localhost:3000/hospital/"
        self.payload = {}
        self.headers = {}
        self.response = None

    def get_hospitals(self):
        self.response = requests.request("GET", self.url, headers=self.headers, data=self.payload)
        self.hospitals = json.loads(self.response.text)
        print(self.hospitals)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Search Hospital'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        self.get_hospitals()

        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

        hospitals = ListView(
            expand=True,
        )

        for i in range(len(self.hospitals)):
            hospitals.controls.append(
                Container(
                    content=Text('test')
                )
            )

        return View(
            route="/searchHospital",
            padding=50,
            controls=[
                Column(
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.WHITE,
                                    on_click=go_select_hospital
                                ),
                                Text(value='Search Hospital',
                                     style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        hospitals
                    ]
                )
            ]
        )

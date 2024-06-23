import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr
import requests
import json

# Initialize global variables
selected_container = None
doctor_id = None


class SelectDoctor:
    def __init__(self):
        self.doctorsURL = "http://localhost:3000/doctor"
        self.doctor_payload = {}
        self.doctor_headers = {}
        self.doctor_response = None
        self.doctors = None

    # Fetches doctors for the specified hospital ID
    def get_doctors(self, hospital_id):
        full_url = f"{self.doctorsURL}/{hospital_id}"
        self.doctor_response = requests.get(full_url, headers=self.doctor_headers, data=self.doctor_payload)
        self.doctors = json.loads(self.doctor_response.text)['doctors']

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        svr.get_doctor_details(hospital_id),
        self.get_doctors(hospital_id)

        # Navigate to doctor info page
        def go_doctor_info(e):
            page.go(f'/doctor/info/{e.control.data}')
            page.update()

        # Navigate to select hospital page
        def go_select_hospital(e):
            global selected_container
            selected_container = None

            page.go("/selectHospital")
            page.update()

        # Navigate to select datetime page
        def go_select_datetime(e):
            global selected_container
            selected_container = None

            if doctor_id is not None:
                page.go(f'/selectDateTime/{hospital_id}/{doctor_id}')
                page.update()

        # Handle tap event on a doctor's card
        def on_tap(e):
            global selected_container
            global doctor_id

            # Deselect previously selected doctor if any
            if selected_container is not None and selected_container != e.control:
                selected_container.content.border = None
                selected_container.update()

            # Toggle selection of the current doctor's card
            if e.control.content.border is None or selected_container != e.control:
                e.control.content.border = border.all(10, colors.BLUE_100)
                selected_container = e.control
                doctor_id = e.control.data
            else:
                e.control.content.border = None
                selected_container = None

            e.control.update()

        doctor = GridView(
            runs_count=3,
            child_aspect_ratio=8/9,
            spacing=30,
            padding=30,
        )

        # Function to display next button
        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(
                                text="Next", style=ButtonStyle(color=colors.GREY_800),
                                icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.GREY_800,
                                on_click=go_select_datetime
                            )
                        ]
                    ),
                ],
            )

        for i in range(len(self.doctors)):
            # Determine doctor's image or default icon
            image_src = self.doctors[i]["image"]
            doctor_image = Image(src=image_src, fit=ImageFit.FIT_HEIGHT) if image_src else Icon(icons.PERSON, color='black', size=140)

            doctor.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    data=int(self.doctors[i]["doctorID"]),
                    content=Container(
                        border_radius=10,
                        bgcolor=colors.WHITE,
                        content=Container(
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Row(
                                        expand=1,
                                        alignment=MainAxisAlignment.END,
                                        controls=[
                                            IconButton(
                                                data=self.doctors[i]["doctorID"],
                                                icon=icons.INFO,
                                                icon_color='grey',
                                                on_click=go_doctor_info
                                            ),
                                        ]
                                    ),
                                    Container(
                                        expand=5,
                                        padding=padding.only(top=10),
                                        content=doctor_image,
                                    ),
                                    Column(
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        expand=2,
                                        controls=[
                                            Text(value=f'{self.doctors[i]["name"]}', color=colors.BLACK, size=12),
                                            Text(
                                                value=f'{svr.get_speciality_name(self.doctors[i]["specialityID"])}',
                                                color=colors.BLACK, size=10
                                            ),
                                        ]
                                    )
                                ]
                            )
                        )
                    ),
                )
            )

        return View(
            bgcolor=colors.GREY_200,
            route="/selectDoctor/:hospital_id",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    style=ButtonStyle(color=colors.GREY_800),
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color=colors.GREY_800,
                                    on_click=go_select_hospital
                                ),
                                Text(
                                    value=svr.get_hospital_name(hospital_id),
                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=doctor,
                        ),
                        display_button(),
                    ]
                ),
            ]
        )
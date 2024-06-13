import flet as ft
from flet import *
from flet_route import Params, Basket
import datetime
import calendar
import requests
import json
import pages.server as svr


class AdminHome:
    def __init__(self):
        self.url = "http://localhost:3000/appointment/"
        self.payload = {}
        self.headers = {}
        self.response = None
        self.pending_appointments = None
        self.approved_appointments = None

    def get_pending_appointments(self):
        # Perform the HTTP request to fetch appointments
        self.response = requests.request("GET", self.url + 'pending', headers=self.headers, data=self.payload)
        # Store the response text data
        self.pending_appointments = json.loads(self.response.text)

    def get_approved_appointments(self):
        # Perform the HTTP request to fetch appointments
        self.response = requests.request("GET", self.url + 'approved', headers=self.headers, data=self.payload)
        # Store the response text data
        self.approved_appointments = json.loads(self.response.text)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Admin'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        self.get_pending_appointments()
        self.get_approved_appointments()

        def go_login(e):
            page.go("/")
            page.update()

        def convert_date(timestamp):
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            return dt_object.strftime("%d %B %Y")

        def convert_time(timestamp):
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            return dt_object.strftime("%I:%M %p")

        def approve_appointment(book_id):
            url = "http://localhost:3000/approveAppointment/"

            payload = f'bookID={book_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url + str(book_id), headers=headers, data=payload)
            print(response.text)

            page.go("/adminHome")
            page.update()

        def delete_appointment(book_id):
            url = "http://localhost:3000/appointment/pending/delete/"

            payload = f'bookID={book_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url + str(book_id), headers=headers, data=payload)
            print(response.text)

            page.go("/adminHome")
            page.update()

        pending_appointments = ListView(
            expand=True,
        )

        approved_appointments = ListView(
            expand=True,
        )

        for i in range(len(self.pending_appointments)):
            pending_appointments.controls.append(
                Container(
                    padding=5,
                    content=Container(
                        border_radius=10,
                        bgcolor="amber",
                        padding=padding.only(left=10, top=5, bottom=5),
                        width=400,
                        height=125,
                        content=Row(
                            expand=True,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Container(
                                    expand=2,
                                    content=Column(
                                        expand=True,
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.DATE_RANGE_OUTLINED, color="white"),
                                                        Text(value=f'{convert_date(self.pending_appointments[i]["datetime"])}', color="white")
                                                    ]
                                                ),
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.ACCESS_TIME_OUTLINED, color="white"),
                                                        Text(value=f'{convert_time(self.pending_appointments[i]["datetime"])}', color="white")
                                                    ]
                                                )
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.LOCAL_HOSPITAL_OUTLINED, color="white"),
                                                        Text(value=f'{svr.get_hospital_name(self.pending_appointments[i]["hospitalID"])}',
                                                             color="white")
                                                    ]
                                                )
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.PEOPLE_OUTLINED, color="white"),
                                                        Text(value=f'{svr.get_doctor_name(self.pending_appointments[i]["doctorID"])}',
                                                             color="white")
                                                    ]
                                                )
                                            ),
                                        ]

                                    )
                                ),
                                Container(
                                    expand=1,
                                    content=Column(
                                        alignment=MainAxisAlignment.SPACE_EVENLY,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Row(
                                                alignment=MainAxisAlignment.START,
                                                controls=[
                                                    IconButton(icon=icons.CHECK_OUTLINED, icon_size=35,
                                                               icon_color="white", on_click=lambda e: approve_appointment(self.pending_appointments[i]["bookID"])),
                                                    TextButton(text="Approve", style=ButtonStyle(color=colors.WHITE), on_click=lambda e: approve_appointment(self.pending_appointments[i]["bookID"]))
                                                ]
                                            ),
                                            Row(
                                                controls=[
                                                    IconButton(icon=icons.DO_NOT_DISTURB_OUTLINED, icon_size=35,
                                                               icon_color="white", on_click=lambda e: delete_appointment(self.pending_appointments[i]["bookID"])),
                                                    TextButton(text="Reject", style=ButtonStyle(color=colors.WHITE), on_click=lambda e: delete_appointment(self.pending_appointments[i]["bookID"]))
                                                ]
                                            ),
                                        ]
                                    )
                                )
                            ]
                        ),
                    ),
                ),
            )

        for i in range(len(self.approved_appointments)):
            approved_appointments.controls.append(
                Container(
                    padding=5,
                    content=Container(
                        border_radius=10,
                        bgcolor="amber",
                        padding=padding.only(left=10, top=5, bottom=5),
                        width=400,
                        height=125,
                        content=Row(
                            expand=True,
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Container(
                                    expand=True,
                                    content=Column(
                                        expand=True,
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        controls=[
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.DATE_RANGE_OUTLINED, color="white"),
                                                        Text(value=f'{convert_date(self.approved_appointments[i]["datetime"])}', color="white")
                                                    ]
                                                ),
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.ACCESS_TIME_OUTLINED, color="white"),
                                                        Text(value=f'{convert_time(self.approved_appointments[i]["datetime"])}', color="white")
                                                    ]
                                                )
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.LOCAL_HOSPITAL_OUTLINED, color="white"),
                                                        Text(value=f'{svr.get_hospital_name(self.approved_appointments[i]["hospitalID"])}',
                                                             color="white")
                                                    ]
                                                )
                                            ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(name=icons.PEOPLE_OUTLINED, color="white"),
                                                        Text(value=f'{svr.get_doctor_name(self.approved_appointments[i]["doctorID"])}',
                                                             color="white")
                                                    ]
                                                )
                                            ),
                                        ]

                                    )
                                ),
                            ]
                        ),
                    ),
                ),
            )

        return View(
            route="/adminHome",
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    controls=[
                        Container(
                            padding=padding.only(right=5),
                            content=Column(
                                controls=[
                                    Container(
                                        expand=True,
                                        border_radius=10,
                                        width=200,
                                        bgcolor=colors.GREY_800,
                                        content=Column(
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                Container(
                                                    padding=10,
                                                    content=Column(
                                                        controls=[
                                                            TextButton(
                                                                text='Admin',
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.PERSON,
                                                            ),
                                                            TextButton(
                                                                text='Hospitals',
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.LOCAL_HOSPITAL_OUTLINED,
                                                                # on_click=
                                                            ),
                                                            TextButton(
                                                                text='Doctors',
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.PERSON_PIN_OUTLINED,
                                                                # on_click=
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                                Container(
                                                    padding=10,
                                                    content=TextButton(
                                                        text='Logout',
                                                        style=ButtonStyle(color=colors.WHITE),
                                                        icon=icons.LOGOUT_OUTLINED,
                                                        on_click=go_login
                                                    ),
                                                ),
                                            ]
                                        )
                                    ),
                                ]
                            ),
                        ),
                        Column(
                            expand=True,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Pending Appointment', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                pending_appointments
                            ]
                        ),
                        Column(
                            expand=True,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Approved Appointment', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                approved_appointments
                            ]
                        ),
                    ]
                ),
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import pages.server as svr


class AdminHome:
    def __init__(self):
        self.url = "http://localhost:3000/appointment/hospital"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.appointments = None

    def get_appointments(self, hospital_id):
        full_url = f"{self.url}/{hospital_id}"
        print(full_url)
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        self.appointments = json.loads(self.response.text)
        print(self.appointments)

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Admin'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        svr.get_doctor_details(hospital_id)
        self.get_appointments(hospital_id)

        def go_login(e):
            page.go("/")
            page.update()

        def approve_dlg_modal(e):
            book_id = e.control.data

            for i in range(len(self.appointments)):
                if self.appointments[i]["bookID"] == book_id:
                    date = svr.convert_date(self.appointments[i]["datetime"])
                    time = svr.convert_time(self.appointments[i]["datetime"])
                    hospital = svr.get_hospital_name(self.appointments[i]["hospitalID"])
                    doctor = svr.get_doctor_name(self.appointments[i]["doctorID"])

            dlg_modal = AlertDialog(
                modal=False,
                title=Text("Approve Appointment"),
                content=Text("Are you sure?"),
                actions=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(value=date),
                                Text(value=time),
                                Text(value=hospital),
                                Text(value=doctor),
                                TextButton(text='Approve', width=150, on_click=lambda e: (approve_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
                            ]
                        ))
                ],
                actions_alignment=MainAxisAlignment.CENTER,
            )

            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def reject_dlg_modal(e):
            book_id = e.control.data

            for i in range(len(self.appointments)):
                if self.appointments[i]["bookID"] == book_id:
                    date = svr.convert_date(self.appointments[i]["datetime"])
                    time = svr.convert_time(self.appointments[i]["datetime"])
                    hospital = svr.get_hospital_name(self.appointments[i]["hospitalID"])
                    doctor = svr.get_doctor_name(self.appointments[i]["doctorID"])

            dlg_modal = AlertDialog(
                modal=False,
                title=Text("Reject Appointment"),
                content=Text("Are you sure?"),
                actions=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(value=date),
                                Text(value=time),
                                Text(value=hospital),
                                Text(value=doctor),
                                TextButton(text='Reject', width=150, on_click=lambda e: (reject_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
                            ]
                        ))
                ],
                actions_alignment=MainAxisAlignment.CENTER,
            )

            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def approve_appointment(book_id):
            url = f"http://localhost:3000/appointment/approve/{book_id}"
            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

        def reject_appointment(book_id):
            url = f"http://localhost:3000/appointment/reject/{book_id}"
            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

        appointments = ListView(
            expand=True,
        )

        for i in range(len(self.appointments)):
            if self.appointments[i]["status"] == 0:
                colour = 'grey'
                status = 'PENDING'
                disable = False
            elif self.appointments[i]["status"] == 1:
                colour = 'green'
                status = 'APPROVED'
                disable = True
            else:
                colour = 'red'
                status = 'REJECTED'
                disable = True

            appointments.controls.append(
                Container(
                    padding=5,
                    content=Container(
                        border_radius=10,
                        bgcolor=colour,
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
                                                        Text(value=f'{svr.convert_date(self.appointments[i]["datetime"])}', color="white")
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
                                                        Text(value=f'{svr.convert_time(self.appointments[i]["datetime"])}', color="white")
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
                                                        Text(value=f'{svr.get_hospital_name(self.appointments[i]["hospitalID"])}',
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
                                                        Text(value=f'{svr.get_doctor_name(self.appointments[i]["doctorID"])}',
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
                                                        Icon(icons.EDIT_DOCUMENT, color='white'),
                                                        Text(status, color='white')
                                                    ]
                                                )
                                            ),
                                        ]
                                    )
                                ),
                                Row(
                                    expand=1,
                                    alignment=MainAxisAlignment.SPACE_EVENLY,
                                    controls=[
                                        GestureDetector(
                                            mouse_cursor=MouseCursor.CLICK,
                                            data=int(self.appointments[i]["bookID"]),
                                            on_tap=approve_dlg_modal if not disable else None,
                                            content=Container(
                                                expand=True,
                                                content=Column(
                                                    alignment=MainAxisAlignment.CENTER,
                                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        Icon(icons.CHECK_OUTLINED, size=35, color="white"),
                                                        Text(value="Approve", color=colors.WHITE),
                                                    ]
                                                )
                                            )
                                        ),
                                        GestureDetector(
                                            mouse_cursor=MouseCursor.CLICK,
                                            data=int(self.appointments[i]["bookID"]),
                                            on_tap=reject_dlg_modal if not disable else None,
                                            content=Container(
                                                expand=True,
                                                content=Column(
                                                    alignment=MainAxisAlignment.CENTER,
                                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                                    controls=[
                                                        Icon(icons.DO_NOT_DISTURB_OUTLINED, size=35,
                                                             color="white"),
                                                        Text(value="Reject", color=colors.WHITE),
                                                    ]
                                                )
                                            )
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ),
                ),
            )

        doctors = GridView(
            expand=True,
        )

        for i in range(len(svr.doctorFilteredList)):
            doctors.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    # on_tap=,
                    data=int(svr.doctorFilteredList[i]["doctorID"]),
                    content=Container(
                        border_radius=10,
                        bgcolor="white",
                        content=Container(
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        expand=3,
                                        padding=padding.only(top=10),
                                        content=Image(src=f'{svr.doctorFilteredList[i]["image"]}', fit=ImageFit.FIT_HEIGHT),
                                    ),
                                    Column(
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        expand=1,
                                        controls=[
                                            Text(value=f'{svr.doctorFilteredList[i]["name"]}', color='black', size=12),
                                            Text(value=f'{svr.get_speciality_name(svr.doctorFilteredList[i]["specialityID"])}',
                                                 color='black', size=10),
                                        ]
                                    )
                                ]
                            )
                        )
                    ),
                )
            )

        return View(
            route="/adminHome/:hospital_id",
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
                                                                text=f'{svr.get_hospital_name(hospital_id)}',
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.PERSON,
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
                            expand=2,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Appointment', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                appointments
                            ]
                        ),
                        Column(
                            expand=1,
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                ElevatedButton(text='Add Doctor'),
                                doctors
                            ]
                        ),
                    ]
                ),
            ]
        )
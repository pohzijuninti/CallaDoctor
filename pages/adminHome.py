import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import pages.server as svr

new_specialityID = None


class AdminHome:
    def __init__(self):
        self.appointmentURL = "http://localhost:3000/appointment/hospital"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.appointments = None

        self.doctorsURL = "http://localhost:3000/doctor"
        self.doctor_payload = {}
        self.doctor_headers = {}
        self.doctor_response = None
        self.doctors = None

    def get_appointments(self, hospital_id):
        full_url = f"{self.appointmentURL}/{hospital_id}"
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        self.appointments = json.loads(self.response.text)

    def get_doctors(self, hospital_id):
        full_url = f"{self.doctorsURL}/{hospital_id}"
        self.doctor_response = requests.get(full_url, headers=self.doctor_headers, data=self.doctor_payload)
        self.doctors = json.loads(self.doctor_response.text)['doctors']

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Admin'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        svr.get_doctor_details(hospital_id)
        self.get_appointments(hospital_id)
        self.get_doctors(hospital_id)

        def close_anchor(e):
            global new_specialityID
            new_specialityID = e.control.data
            print(new_specialityID)
            anchor.close_view(svr.specialityList[e.control.data - 11]["name"])

        new_name: TextField = TextField(icon=icons.PERSON, label='Name', border=InputBorder.UNDERLINE, text_size=14)
        new_email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', border=InputBorder.UNDERLINE, text_size=14)
        anchor = SearchBar(
            width=300,
            bar_hint_text='Select Speciality',
            bar_leading=Container(
                content=Icon(icons.LOCAL_HOSPITAL_OUTLINED, color=colors.WHITE),
            ),
            controls=[
                ListTile(
                    title=Text(f'{svr.specialityList[i]["name"]}'),
                    on_click=close_anchor,
                    data=int(svr.specialityList[i]["specialityID"])
                )
                for i in range(len(svr.specialityList))
            ]
        )

        def go_login(e):
            page.go("/")
            page.update()

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def add_doctor(name, hospitalID, email):
            try:
                url = "http://localhost:3000/doctor/add"

                payload = f'name={name}&specialityID={new_specialityID}&hospitalID={hospitalID}&email={email}'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                new_doctor = json.loads(response.text)['doctor']
                self.doctors.append(new_doctor)

                # Update doctors GridView
                update_doctors_view()

                page.update()
            except Exception as e:
                print('Add doctor failed', e)
            return

        def done(e):
            dlg_modal.open = False
            add_doctor(new_name.value, hospital_id, new_email.value)
            new_name.value = ""
            anchor.data = ""
            new_email.value = ""
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Add Doctor"),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            new_name,
                            new_email,
                            anchor,
                            Container(
                                padding=padding.only(top=20, bottom=10),
                                content=ElevatedButton(text="Done", on_click=done, width=250)
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        appointments = ListView(
            expand=True,
        )

        doctors = GridView(
            expand=True,
        )

        def update_appointments_view():
            appointments.controls.clear()  # Clear existing controls
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

                userID = self.appointments[i]['userID']
                url = f"http://localhost:3000/username/{userID}"

                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)
                name = json.loads(response.text)['name']

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
                                                            Icon(name=icons.DATE_RANGE_OUTLINED, color=colors.WHITE),
                                                            Text(
                                                                value=f'{svr.convert_date(self.appointments[i]["datetime"])}',
                                                                color=colors.WHITE)
                                                        ]
                                                    ),
                                                ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(name=icons.ACCESS_TIME_OUTLINED, color=colors.WHITE),
                                                            Text(
                                                                value=f'{svr.convert_time(self.appointments[i]["datetime"])}',
                                                                color=colors.WHITE)
                                                        ]
                                                    )
                                                ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(name=icons.PERSON, color=colors.WHITE),
                                                            Text(value=f'{name}', color=colors.WHITE)
                                                        ]
                                                    )
                                                ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(name=icons.HEALTH_AND_SAFETY, color=colors.WHITE),
                                                            Text(
                                                                value=f'{svr.get_doctor_name(self.appointments[i]["doctorID"])}',
                                                                color=colors.WHITE)
                                                        ]
                                                    )
                                                ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(icons.EDIT_DOCUMENT, color=colors.WHITE),
                                                            Text(status, color=colors.WHITE)
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
                                                            Icon(name='done', size=35, color=colors.WHITE),
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
                                                            Icon(name=icons.DO_NOT_DISTURB_OUTLINED, size=35, color=colors.WHITE),
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
            page.update()

        def update_doctors_view():
            doctors.controls.clear()  # Clear existing controls
            for i in range(len(self.doctors)):
                speciality = svr.get_speciality_name(self.doctors[i]["specialityID"])
                doctors.controls.append(
                    Container(
                        border_radius=10,
                        bgcolor=colors.WHITE,
                        content=Container(
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    GestureDetector(
                                        mouse_cursor=MouseCursor.CLICK,
                                        data=int(self.doctors[i]["doctorID"]),
                                        # on_tap=on_tap,
                                        content=Container(
                                            padding=padding.only(top=5, right=5),
                                            alignment=alignment.top_right,
                                            content=Icon(icons.DELETE_OUTLINED, color=colors.BLACK),
                                        )
                                    ),
                                    Container(
                                        expand=2,
                                        content=display_doc_image(self.doctors[i]["image"]),
                                    ),
                                    Column(
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        expand=1,
                                        controls=[
                                            Text(value=f'{self.doctors[i]["name"]}', color=colors.BLACK, size=12),
                                            Text(value=f'{speciality}', color=colors.BLACK, size=10),
                                        ]
                                    )
                                ]
                            )
                        )
                    ),
                )
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
                                TextButton(text='Approve', width=150, on_click=lambda e: (
                                approve_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
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
                                TextButton(text='Reject', width=150, on_click=lambda e: (
                                reject_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
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

            # Refresh appointments data and update the view
            self.get_appointments(hospital_id)
            update_appointments_view()

        def reject_appointment(book_id):
            url = f"http://localhost:3000/appointment/reject/{book_id}"
            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            # Refresh appointments data and update the view
            self.get_appointments(hospital_id)
            update_appointments_view()

        def display_doc_image(img):
            if img == "":
                return Icon(icons.PERSON, color=colors.BLACK, size=140)
            else:
                return Image(src=f'{img}', fit=ImageFit.FIT_HEIGHT)

        update_doctors_view()  # Initialize the GridView with current doctors
        update_appointments_view()  # Initialize the ListView with current appointments

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
                                ElevatedButton(text='Add Doctor', on_click=open_dlg_modal),
                                doctors
                            ]
                        ),
                    ]
                ),
            ]
        )

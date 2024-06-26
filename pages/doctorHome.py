import flet as ft
from flet import *
from flet_route import Params, Basket
import datetime
import calendar
import requests
import json
import pages.server as svr


class DoctorHome:
    def __init__(self):
        self.calendar_grid = None

        self.appointmentURL = "http://localhost:3000/appointment/doctor"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.appointments = None
        self.booking_histories = None
        self.hospital_id = None

    # Fetches appointments for the specified doctor ID
    def get_appointments(self, doctor_id):
        full_url = f"{self.appointmentURL}/{doctor_id}"
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        self.appointments = json.loads(self.response.text)

    # Separate booking histories from upcoming appointments
    def get_booking_histories(self):
        self.booking_histories = []
        i = 0
        while i < len(self.appointments):
            if self.appointments[i]["datetime"] < datetime.datetime.now().timestamp():
                self.booking_histories.append(self.appointments[i])
                del self.appointments[i]
            else:
                i += 1

    # Generate the calendar view
    def generate_calendar(self, page):
        current_date = datetime.date.today()
        current_year = current_date.year
        current_month = current_date.month

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        for month in range(current_month, current_month + 1):
            month_label = Container(
                margin=margin.only(bottom=-10),
                alignment=alignment.center,
                content=Text(
                    f"{calendar.month_name[month]} {current_year}",
                    size=14,
                    weight=FontWeight.BOLD,
                    color=colors.BLACK,
                    text_align=TextAlign.CENTER
                )
            )

            month_matrix = calendar.monthcalendar(current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER,
                                spacing=25)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[month_label]
                )
            )

            weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            weekday_row = Row()
            for weekday in weekday_labels:
                day_container = Container(
                    width=20,
                    height=20,
                    alignment=alignment.center,
                    content=Text(weekday, size=9, color=colors.BLACK),
                    margin=margin.only(right=10, bottom=-10)
                )
                weekday_row.controls.append(day_container)

            month_grid.controls.append(weekday_row)

            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day == 0:
                        day_container = Container(
                            width=20,
                            height=20,
                            alignment=alignment.center,
                            content=None,
                            margin=margin.only(right=10)
                        )
                    else:
                        day_container = Container(
                            width=20,
                            height=20,
                            border=None,
                            alignment=alignment.center,
                            content=Text(str(day), size=12, color=colors.BLACK, weight=FontWeight.W_500),
                            margin=margin.only(right=10, bottom=-10),
                        )

                    if day == current_date.day and month == current_date.month and current_year == current_date.year:
                        day_container.border_radius = 14
                        day_container.bgcolor = colors.RED
                        day_container.content.color = colors.WHITE
                        day_container.content.color = colors.WHITE

                    if day < current_date.day:
                        if day_container.content:
                            day_container.content.color = colors.GREY_500
                            day_container.disabled = True

                    week_container.controls.append(day_container)

                month_grid.controls.append(week_container)

            self.calendar_grid.controls.append(month_grid)

        return Container(
            border_radius=10,
            bgcolor=colors.WHITE,
            padding=padding.only(left=5, right=5, top=15, bottom=15),
            content=Container(
                alignment=alignment.center,
                margin=margin.only(left=10, right=10),
                content=self.calendar_grid  # Use self.calendar_grid here
            )
        )

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        doctor_id = int(params.doctor_id)
        self.get_appointments(doctor_id)
        self.get_booking_histories()

        # Navigate to login page
        def go_login(e):
            page.go("/")
            page.update()

        # Navigate to the patient list page for a specific doctor at a hospital
        def go_patient_list(hospital_id, doctor_id):
            page.go(f"/doctor/patientList/{hospital_id}/{doctor_id}")
            page.update()

        # Navigate to the medical record page for a specific patient with a doctor at a hospital
        def go_doctor_medical_record(hospital_id, user_id):
            page.go(f"/doctorMedicalRecord/{hospital_id}/{doctor_id}/{user_id}")
            page.update()

        appointments = ListView(
            expand=True,
        )

        booking_history = ListView(
            expand=True,
            spacing=10,
        )

        # Update the appointments view
        def update_appointments_view():
            appointments.controls.clear()

            # Sort by date then time
            self.appointments.sort(
                key=lambda appt: (
                    svr.convert_date(appt["datetime"]),
                    svr.convert_time(appt["datetime"])
                )
            )

            for i in range(len(self.appointments)):
                userID = self.appointments[i]['userID']
                hospitalID = self.appointments[i]['hospitalID']

                if self.appointments[i]["status"] == 0:
                    colour = 'grey'
                    colour1 = 'white'
                    colour2 = 'white'
                    icon1 = 'done'
                    text1 = 'Approve'
                    icon2 = 'do_not_disturb'
                    text2 = 'Reject'
                    status = 'PENDING'
                    action1 = approve_dlg_modal
                    action2 = reject_dlg_modal
                elif self.appointments[i]["status"] == 1:
                    colour = 'green'
                    colour1 = 'green'
                    colour2 = 'white'
                    icon1 = 'done'
                    text1 = 'Approve'
                    icon2 = 'edit_document'
                    text2 = 'Record'
                    status = 'APPROVED'
                    action1 = None
                    action2 = lambda e: go_doctor_medical_record(hospitalID, userID)
                else:
                    colour = 'red'
                    colour1 = 'red'
                    colour2 = 'red'
                    icon1 = 'done'
                    text1 = 'Approve'
                    icon2 = 'do_not_disturb'
                    text2 = 'Reject'
                    status = 'REJECTED'
                    action1 = None
                    action2 = None

                # Construct the URL to fetch user details based on userID.
                url = f"http://localhost:3000/user/{userID}"
                payload = {}
                headers = {}

                # Send a GET request to the server to retrieve user information.
                response = requests.request("GET", url, headers=headers, data=payload)
                # Extract the user's name from the response JSON data.
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
                                                            Icon(name=icons.LOCAL_HOSPITAL_OUTLINED, color=colors.WHITE),
                                                            Text(
                                                                value=f'{svr.get_hospital_name(self.appointments[i]["hospitalID"])}',
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
                                                on_tap=action1,
                                                content=Container(
                                                    expand=True,
                                                    content=Column(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            Icon(name=icon1, size=35, color=colour1),
                                                            Text(value=text1, color=colour1),
                                                        ]
                                                    )
                                                )
                                            ),
                                            GestureDetector(
                                                mouse_cursor=MouseCursor.CLICK,
                                                data=int(self.appointments[i]["bookID"]),
                                                on_tap=action2,
                                                content=Container(
                                                    expand=True,
                                                    content=Column(
                                                        alignment=MainAxisAlignment.CENTER,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        controls=[
                                                            Icon(name=icon2, size=35, color=colour2),
                                                            Text(value=text2, color=colour2),
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

        # Update the booking histories view
        def update_bookingHistories_view():
            booking_history.controls.clear()

            self.booking_histories = sorted(self.booking_histories, key=lambda appt: appt["datetime"], reverse=True)[:10]

            for i in range(len(self.booking_histories)):
                userID = self.booking_histories[i]['userID']

                url = f"http://localhost:3000/user/{userID}"

                payload = {}
                headers = {}

                response = requests.request("GET", url, headers=headers, data=payload)
                name = json.loads(response.text)['name']

                booking_history.controls.append(
                    Container(
                        content=Container(
                            border_radius=10,
                            bgcolor="white",
                            padding=5,
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
                                                            Icon(
                                                                name=icons.DATE_RANGE_OUTLINED,
                                                                color=colors.GREY,
                                                                size=20),
                                                            Text(
                                                                value=f'{svr.convert_date(self.booking_histories[i]["datetime"])}',
                                                                color=colors.GREY_700,
                                                                size=10)
                                                        ]
                                                    ),
                                                ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(
                                                                name=icons.ACCESS_TIME_OUTLINED,
                                                                color=colors.GREY,
                                                                size=20),
                                                            Text(
                                                                value=f'{svr.convert_time(self.booking_histories[i]["datetime"])}',
                                                                color=colors.GREY_700,
                                                                size=10)
                                                        ]
                                                    )
                                                ),
                                            Container(
                                                expand=True,
                                                content=Row(
                                                    expand=True,
                                                    alignment=MainAxisAlignment.START,
                                                    controls=[
                                                        Icon(
                                                            name=icons.LOCAL_HOSPITAL_OUTLINED,
                                                            color=colors.GREY,
                                                            size=20),
                                                        Text(
                                                            value=f'{svr.get_hospital_name(self.booking_histories[i]["hospitalID"])}',
                                                            color=colors.GREY_700,
                                                            size=10)
                                                    ]
                                                )
                                            ),
                                                Container(
                                                    expand=True,
                                                    content=Row(
                                                        expand=True,
                                                        alignment=MainAxisAlignment.START,
                                                        controls=[
                                                            Icon(
                                                                name=icons.PERSON,
                                                                color=colors.GREY,
                                                                size=20),
                                                            Text(
                                                                value=f'{name}',
                                                                color=colors.GREY_700,
                                                                size=10)
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
            page.update()

        # Opens the modal dialog for approving an appointment
        def approve_dlg_modal(e):
            book_id = e.control.data  # Get the booking ID from the control's data

            # Find the appointment details for the given booking ID
            for i in range(len(self.appointments)):
                if self.appointments[i]["bookID"] == book_id:
                    date = svr.convert_date(self.appointments[i]["datetime"])
                    time = svr.convert_time(self.appointments[i]["datetime"])
                    hospital = svr.get_hospital_name(self.appointments[i]["hospitalID"])
                    userID = self.appointments[i]["userID"]

            # Construct the URL to fetch user details based on userID.
            url = f"http://localhost:3000/user/{userID}"
            payload = {}
            headers = {}

            # Send a GET request to the server to retrieve user information.
            response = requests.request("GET", url, headers=headers, data=payload)
            # Extract the user's name from the response JSON data.
            name = json.loads(response.text)['name']

            dlg_modal = AlertDialog(
                modal=False,
                title=Text("Approve Appointment"),
                content=Text("Are you sure?", text_align=TextAlign.CENTER),
                actions=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(value=date),
                                Text(value=time),
                                Text(value=hospital),
                                Text(value=name),
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
            book_id = e.control.data  # Get the booking ID from the control's data

            # Find the appointment details for the given booking ID
            for i in range(len(self.appointments)):
                if self.appointments[i]["bookID"] == book_id:
                    date = svr.convert_date(self.appointments[i]["datetime"])
                    time = svr.convert_time(self.appointments[i]["datetime"])
                    hospital = svr.get_hospital_name(self.appointments[i]["hospitalID"])
                    userID = self.appointments[i]["userID"]

            # Construct the URL to fetch user details based on userID.
            url = f"http://localhost:3000/user/{userID}"
            payload = {}
            headers = {}

            # Send a GET request to the server to retrieve user information.
            response = requests.request("GET", url, headers=headers, data=payload)
            # Extract the user's name from the response JSON data.
            name = json.loads(response.text)['name']

            dlg_modal = AlertDialog(
                modal=False,
                title=Text("Reject Appointment"),
                content=Text("Are you sure?", text_align=TextAlign.CENTER),
                actions=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(value=date),
                                Text(value=time),
                                Text(value=hospital),
                                Text(value=name),
                                TextButton(text='Reject', width=150, on_click=lambda e: (reject_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
                            ]
                        ))
                ],
                actions_alignment=MainAxisAlignment.CENTER,
            )

            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        # Approve the appointment with the specified book ID
        def approve_appointment(book_id):
            url = f"http://localhost:3000/appointment/approve/{book_id}"
            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)

            self.get_appointments(doctor_id)
            update_appointments_view()

        # Reject the appointment with the specified book ID
        def reject_appointment(book_id):
            url = f"http://localhost:3000/appointment/reject/{book_id}"
            payload = {}
            headers = {}

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)

            self.get_appointments(doctor_id)
            update_appointments_view()

        # Format a description string
        def display_description(description):
            if ',' in description:
                description = description.replace(',', '\n*')
            if not description.startswith('*'):
                description = '* ' + description
            return description

        update_appointments_view()   # Initialize the GridView with current appointments
        update_bookingHistories_view()   # Initialize the GridView with current booking histories

        return View(
            bgcolor=colors.GREY_200,
            route="/doctorHome/:doctor_id",
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
                                        bgcolor=colors.GREY_400,
                                        content=Column(
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                Container(
                                                    padding=10,
                                                    content=Column(
                                                        controls=[
                                                            TextButton(
                                                                text=f'{svr.get_doctor_name(doctor_id)}',
                                                                style=ButtonStyle(color=colors.BLACK),
                                                                icon=icons.PERSON,
                                                            ),
                                                            TextButton(
                                                                text='Patient List',
                                                                style=ButtonStyle(color=colors.BLACK),
                                                                icon=icons.PEOPLE_OUTLINED,
                                                                on_click=lambda e: go_patient_list(self.hospital_id, doctor_id)
                                                            ),
                                                        ]
                                                    ),
                                                ),
                                                Container(
                                                    padding=10,
                                                    content=TextButton(
                                                        text='Logout',
                                                        style=ButtonStyle(color=colors.BLACK),
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
                                    padding=padding.only(left=10),
                                    content=Text(value='Appointment', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                appointments
                            ]
                        ),
                        Column(
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                Container(
                                    expand=True,
                                    padding=padding.only(left=5, top=5),
                                    content=
                                    Column(
                                        expand=True,
                                        controls=[
                                            Container(
                                                content=Container(
                                                    border_radius=10,
                                                    width=300,
                                                    height=300,
                                                    content=self.generate_calendar(page),
                                                ),
                                            ),
                                            Row(
                                                expand=True,
                                                controls=[
                                                    Column(
                                                        controls=[
                                                            Container(
                                                                content=Text(
                                                                    value='Booking History',
                                                                    style=TextStyle(size=18, weight=FontWeight.BOLD)
                                                                ),
                                                            ),
                                                            Container(
                                                                expand=True,
                                                                border_radius=10,
                                                                width=300,
                                                                height=100,
                                                                content=booking_history
                                                            ),
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent
from db.config import register, login
import datetime
import calendar
import requests
import json
from db.config import get_name, get_userID
import pages.server as svr


class Home:
    def __init__(self):
        self.calendar_grid = None
        self.url = "http://localhost:3000/appointment"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.appointments = None

    def get_appointments(self):
        full_url = f"{self.url}/{get_userID()}"
        print(full_url)
        # Perform the HTTP request to fetch appointments
        self.response = requests.get(full_url, headers=self.headers, data=self.payload)
        # Store the response text data
        self.appointments = json.loads(self.response.text)
        print(self.appointments)

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
                    content=Text(weekday, size=12, color=colors.BLACK),
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

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        self.get_appointments()
        name = get_name()

        def go_login(e):
            page.go("/")
            page.update()

        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

        def go_medical_record(e):
            page.go("/medicalRecord")
            page.update()

        def convert_date(timestamp):
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            return dt_object.strftime("%d %B %Y")

        def convert_time(timestamp):
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            return dt_object.strftime("%I:%M %p")

        def open_dlg_modal(date, time, hospital, doctor, book_id):
            dlg_modal = AlertDialog(
                modal=False,
                title=Text("Delete Appointment"),
                content=Text("Are you sure?"),
                actions=[
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(value=f'{date}'),
                                Text(value=f'{time}'),
                                Text(value=f'{hospital}'),
                                Text(value=f'{doctor}'),
                                TextButton(text='Delete', width=150, on_click=lambda e: (delete_appointment(book_id), setattr(dlg_modal, 'open', False), page.update())),
                            ]
                        ))
                ],
                actions_alignment=MainAxisAlignment.CENTER,
            )

            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def delete_appointment(book_id):
            url = "http://localhost:3000/appointment/approved/delete/"

            payload = f'bookID={book_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url + str(book_id), headers=headers, data=payload)
            print(response.text)

        appointments = ListView(
            expand=True,
        )

        for i in range(len(self.appointments)):
            if self.appointments[i]["status"] == 0:
                colour = 'grey'
                status = 'PENDING'
            elif self.appointments[i]["status"] == 1:
                colour = 'green'
                status = 'APPROVED'
            else:
                colour = 'red'
                status = 'REJECTED'

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
                                                        Text(value=f'{convert_date(self.appointments[i]["datetime"])}', color="white")
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
                                                        Text(value=f'{convert_time(self.appointments[i]["datetime"])}', color="white")
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
                                GestureDetector(
                                    mouse_cursor=MouseCursor.CLICK,
                                    on_tap=lambda e: open_dlg_modal(
                                                           convert_date(self.appointments[i]["datetime"]),
                                                           convert_time(self.appointments[i]["datetime"]),
                                                           svr.get_hospital_name(self.appointments[i]["hospitalID"]),
                                                           svr.get_doctor_name(self.appointments[i]["doctorID"]),
                                                           self.appointments[i]["bookID"]
                                                       ),
                                    content=Container(
                                        padding=20,
                                        expand=1,
                                        content=Column(
                                            alignment=MainAxisAlignment.CENTER,
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            controls=[
                                                Icon(icons.DELETE_OUTLINED, size=35, color="white"),
                                                Text(value="Delete",color=colors.WHITE),
                                            ]
                                        )
                                    )
                                ),
                            ]
                        ),
                    ),
                ),
            )

        return View(
            route="/home",
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
                                                                text=name,
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.PERSON,
                                                            ),
                                                            TextButton(
                                                                text='Medical Record',
                                                                style=ButtonStyle(color=colors.WHITE),
                                                                icon=icons.FILE_COPY_OUTLINED,
                                                                on_click=go_medical_record
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
                                    content=Text(value='Appointment', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                appointments
                            ]
                        ),

                        Column(
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                ElevatedButton(text='Add Appointment', on_click=go_select_hospital),
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
                                                    bgcolor="red",
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
                                                                expand=True,
                                                                border_radius=10,
                                                                bgcolor=colors.GREY_800,
                                                                width=300,
                                                                height=100,
                                                                content=ListView(
                                                                    expand=True,
                                                                    controls=[
                                                                        Container(
                                                                            padding=5,
                                                                            content=Container(
                                                                                border_radius=10,
                                                                                bgcolor="amber",
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
                                                                                                                Icon(name=icons.DATE_RANGE_OUTLINED,
                                                                                                                    color="white", size=20),
                                                                                                                Text(value="Date", color="white", size=10)
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
                                                                                                                    color="white",
                                                                                                                    size=20),
                                                                                                                Text(
                                                                                                                    value="Time",
                                                                                                                    color="white",
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
                                                                                                                    color="white",
                                                                                                                    size=20),
                                                                                                                Text(
                                                                                                                    value="Hospital",
                                                                                                                    color="white",
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
                                                                                                                    name=icons.PEOPLE_OUTLINED,
                                                                                                                    color="white",
                                                                                                                    size=20),
                                                                                                                Text(
                                                                                                                    value="Doctor",
                                                                                                                    color="white",
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
                                                                        Container(
                                                                            padding=5,
                                                                            content=Container(
                                                                                border_radius=10,
                                                                                bgcolor="pink",
                                                                                width=400,
                                                                                height=125,
                                                                                content=Text('Booking History'),
                                                                            ),
                                                                        ),
                                                                    ]
                                                                ),
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
import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr
import datetime
import calendar
import requests
import json
from db.config import get_userID

selected_container = None
selected_date = None
selected_time = None


class SelectDateTime:
    def __init__(self):
        self.calendar_grid = None
        self.chosen_date = None
        self.url = "http://localhost:3000/timeslots"
        self.payload = {}
        self.headers = {}
        self.response = None
        self.timeslots_data = None
        self.page = None
        self.timeslot = None

    # Fetches available time slots for a specific doctor on a given date
    def get_timeslots(self, doctor_id, date):
        full_url = f"{self.url}/{doctor_id}/{date}"
        # Perform the HTTP request to fetch time slots
        self.response = requests.request("GET", full_url, headers=self.headers, data=self.payload)
        # Store the response text data
        self.timeslots_data = json.loads(self.response.text)

    # Generate a calendar UI with clickable dates for selecting appointment date
    def generate_calendar(self, page, doctor_id):
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
                                spacing=20)
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
                    width=28,
                    height=28,
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
                            width=28,
                            height=28,
                            alignment=alignment.center,
                            content=None,
                            margin=margin.only(right=10)
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=None,
                            alignment=alignment.center,
                            on_click=lambda control, date=day: self.date_clicked(doctor_id, date),
                            content=Text(str(day), size=12, color=colors.BLACK, weight=FontWeight.W_500),
                            margin=margin.only(right=10, bottom=-10),
                        )

                    if day == current_date.day and month == current_date.month and current_year == current_date.year:
                        day_container.border_radius = 14
                        day_container.bgcolor = colors.RED
                        day_container.content.color = colors.WHITE

                    if day == self.chosen_date:
                        day_container.border_radius = 14
                        day_container.bgcolor = colors.WHITE
                        day_container.content.color = colors.RED

                    if day < current_date.day:
                        if day_container.content:
                            day_container.content.color = colors.GREY_500
                            day_container.disabled = True

                    week_container.controls.append(day_container)

                month_grid.controls.append(week_container)

            self.calendar_grid.controls.append(month_grid)

        return Container(
            border_radius=10,
            width=350,
            height=300,
            bgcolor=colors.WHITE,
            padding=padding.only(left=10, right=10, top=20, bottom=20),
            content=Container(
                width=330,
                alignment=alignment.center,
                margin=margin.only(left=10, right=10),
                content=self.calendar_grid  # Use self.calendar_grid here
            )
        )

    # Handles click event on a date in the calendar
    def date_clicked(self, doctor_id, date):
        if date:
            # Reset the previously chosen date
            if self.chosen_date:
                self.reset_date_color(self.chosen_date)

            self.chosen_date = date

            # Update the color for the newly chosen date
            for month_grid in self.calendar_grid.controls:
                for week_container in month_grid.controls[1:]:
                    for day_container in week_container.controls:
                        if day_container.content and day_container.content.value == str(date):
                            day_container.border_radius = 14
                            day_container.bgcolor = colors.GREY_200
                            day_container.content.color = colors.RED
                            day_container.update()

            chosen_day = int(self.chosen_date)
            current_date = datetime.date.today()
            timeslot_date = datetime.date(current_date.year, current_date.month, chosen_day).isoformat()

            self.get_timeslots(doctor_id, timeslot_date)
            self.update_timeslots()

    # Resets the appearance of a selected date back to default
    def reset_date_color(self, date):
        # Reset the properties for a specific date
        for month_grid in self.calendar_grid.controls:
            for week_container in month_grid.controls[1:]:
                for day_container in week_container.controls:
                    if day_container.content and day_container.content.value == str(date):
                        day_container.border_radius = None  # Reset the border_radius
                        day_container.bgcolor = None  # Reset the background color
                        day_container.content.color = colors.BLACK  # Reset the text color
                        day_container.update()

    # Update the time slots view
    def update_timeslots(self):
        self.timeslot.controls.clear()

        for i in range(len(self.timeslots_data)):
            time = svr.convert_time(
                self.timeslots_data[i]['slotDate'])  # Unix timestamp, Convert to 12-hour clock format.

            self.timeslot.controls.append(
                GestureDetector(
                    on_tap=self.on_tap,
                    data=self.timeslots_data[i]['slotDate'],
                    mouse_cursor=MouseCursor.CLICK,
                    content=Container(
                        border_radius=10,
                        alignment=alignment.center,
                        bgcolor=colors.WHITE,
                        content=Text(
                            value=time,
                            color=colors.GREY_800,
                            size=12,
                        ),
                    )
                )
            )
        self.page.update()

    # Handles tap event on a time slot
    def on_tap(self, e):
        global selected_container
        global selected_time

        container = e.control.content  # Access the Container inside the GestureDetector

        # Deselect previously selected timeslot if any
        if selected_container is not None and selected_container != container:
            selected_container.bgcolor = colors.WHITE
            selected_container.content.color = colors.GREY_800
            selected_container.update()

        # Toggle selection of the current timeslot's card
        if container.bgcolor == colors.WHITE:
            container.bgcolor = colors.GREY_300
            container.content.color = colors.RED
            selected_container = container
            selected_time = e.control.data
        else:
            container.bgcolor = colors.WHITE
            container.content.color = colors.GREY_800

        container.update()

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        self.page = page
        page.title = 'Call a Doctor - Select Date & Time'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        doctor_id = int(params.doctor_id)
        self.get_timeslots(doctor_id, datetime.date.today().isoformat())

        self.timeslot = GridView(
            runs_count=3,
            child_aspect_ratio=5 / 2,
        )

        # Navigate to select doctor page
        def go_select_doctor(e):
            global selected_container
            selected_container = None

            page.go(f'/selectDoctor/{hospital_id}')
            page.update()

        # Open a confirmation dialog for the selected appointment date and time
        def open_confirm_dlg(e):
            global selected_date
            global selected_time

            # Construct the URL to update the timeslot availability for a specific doctor and time
            url = f"http://localhost:3000/timeslots/update/{doctor_id}/{selected_time}"

            # Prepare the payload to indicate that the timeslot should be blocked
            payload = 'blockDate=1'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Send a POST request to the server to update the timeslot availability
            response = requests.request("POST", url, headers=headers, data=payload)

            confirm_dlg_modal.actions = [
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(value=f'{svr.convert_date(selected_time)}'),
                            Text(value=f'{svr.convert_time(selected_time)}'),
                            Text(value=f'{svr.get_hospital_name(hospital_id)}'),
                            Text(value=f'{svr.get_doctor_name(doctor_id)}'),
                            TextButton(text='Back To Home', width=150, on_click=close_confirm_dlg),
                        ]
                    )
                )
            ]

            # URL for the endpoint where booking information will be sent
            url = "http://localhost:3000/book"

            # Constructing the payload with user ID, hospital ID, doctor ID, and selected appointment datetime
            payload = f'userID={get_userID()}&hospitalID={hospital_id}&doctorID={doctor_id}&datetime={selected_time}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Making a POST request to the specified URL with headers and payload data
            response = requests.request("POST", url, headers=headers, data=payload)

            page.dialog = confirm_dlg_modal
            confirm_dlg_modal.open = True
            page.update()

        # Close the confirmation dialog and navigates to the home page
        def close_confirm_dlg(e):
            global selected_container
            global selected_date
            global selected_time

            selected_container = None
            selected_date = None
            selected_time = None
            self.chosen_date = None

            page.go("/home")
            page.update()

        confirm_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Successful", text_align=TextAlign.CENTER),
            content=Text("Thanks for choosing us.", text_align=TextAlign.CENTER),
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Opens a dialog when no time slot is selected
        def open_error_dlg(e):
            page.dialog = error_dlg_modal
            error_dlg_modal.open = True
            page.update()

        error_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Error", text_align=TextAlign.CENTER),
            content=Text("Please select a time.", text_align=TextAlign.CENTER),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                text='Close', width=150,
                                on_click=lambda e: (setattr(error_dlg_modal, 'open', False), page.update())
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Open the confirmation dialog if a time slot is selected, otherwise opens an error dialog
        def open_dlg_modal(e):
            global selected_time

            if selected_time is None:
                open_error_dlg(e)
            else:
                open_confirm_dlg(e)

        self.update_timeslots()  # Initialize the GridView with current timeslots

        return View(
            bgcolor=colors.GREY_200,
            route="/selectDateTime/:hospital_id/:doctor_id",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    controls=[
                        TextButton(
                            text=f'{svr.get_hospital_name(hospital_id)}, {svr.get_doctor_name(doctor_id)}',
                            style=ButtonStyle(color=colors.GREY_800),
                            icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color=colors.GREY_800, on_click=go_select_doctor
                        ),
                        Row(
                            expand=True,
                            controls=[
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        self.generate_calendar(page, doctor_id),
                                    ]
                                ),
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Container(
                                            height=300,
                                            content=self.timeslot,
                                        )
                                    ]
                                )
                            ]
                        ),
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Column(
                                    expand=True,
                                    horizontal_alignment=CrossAxisAlignment.END,
                                    controls=[
                                        ElevatedButton(text='Confirm Appointment', on_click=open_dlg_modal),
                                    ]
                                ),
                            ],
                        )
                    ]
                ),
            ],
        )
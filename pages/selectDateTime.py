import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr
import datetime
import calendar
import requests
import json

class SelectDateTime:
    def __init__(self):
        self.calendar_grid = None
        self.chosen_date = None
        self.selected_time_slot = None
        self.time_slots_column = None
        self.appointment_date = None
        today = datetime.date.today()
        self.url = "http://localhost:3000/timeslots/21/" + today.isoformat()
        self.payload = {}
        self.headers = {}
        self.response = None
        self.timeslots_data = None

    def get_timeslots(self):
        # Perform the HTTP request to fetch time slots
        self.response = requests.request("GET", self.url, headers=self.headers, data=self.payload)
        # Store the response text data
        self.timeslots_data = json.loads(self.response.text)


    def generate_calendar(self, page):
        current_date = datetime.date.today()
        current_year = current_date.year
        current_month = current_date.month
        days_in_month = calendar.monthrange(current_year, current_month)[1]

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
                    weight="bold",
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
                            on_click=lambda control, date=day: self.date_clicked(date),
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
                            # day_container.bgcolor = colors.GREY_800
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

    def date_clicked(self, date):
        if date:
            # Reset the previously chosen date
            if self.chosen_date:
                self.reset_date_color(self.chosen_date)

            self.chosen_date = date
            print(f"Chosen Date: {self.chosen_date}")

            # Update the color for the newly chosen date
            for month_grid in self.calendar_grid.controls:
                for week_container in month_grid.controls[1:]:
                    for day_container in week_container.controls:
                        if day_container.content and day_container.content.value == str(date):
                            day_container.border_radius = 14
                            day_container.bgcolor = colors.GREY_200
                            day_container.content.color = colors.RED
                            day_container.update()

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

    def generate_time_slots(self, working_time):
        start_time, end_time = working_time.split(" - ")
        start_time = datetime.datetime.strptime(start_time, "%I:%M %p")
        end_time = datetime.datetime.strptime(end_time, "%I:%M %p")

        time_slots = []

        while start_time < end_time:
            end_of_slot = start_time + datetime.timedelta(hours=1.5)
            start_time_str = start_time.strftime("%I:%M %p")
            end_of_slot_str = end_of_slot.strftime("%I:%M %p")

            # Check if the current time slot is the selected time slot
            is_selected = start_time_str == self.selected_time_slot

            # Define the button's bgcolor based on selection
            bgcolor = colors.WHITE if is_selected else "#3386C5"
            text_color = "#3386C5" if is_selected else colors.WHITE

            def on_time_slot_click(control, time=start_time_str):
                self.time_slot_clicked(control, time, is_selected)

            time_slot_button = Container(
                margin=margin.only(left=10, bottom=5),
                content=TextButton(
                    content=Text(start_time_str, size=14, color=text_color, font_family="RobotoSlab"),
                    width=95,
                    height=45,
                    style=ButtonStyle(bgcolor={"": bgcolor}, shape={"": RoundedRectangleBorder(radius=7)},
                                      side={"": BorderSide(1, "#3386C5")}, ),
                    on_click=on_time_slot_click,
                )
            )

            time_slots.append(time_slot_button)

            start_time = end_of_slot

        rows = [time_slots[i:i + 3] for i in range(0, len(time_slots), 3)]

        self.time_slots_column = Column(
            controls=[Row(controls=row, spacing=10) for row in rows]
        )

        return self.time_slots_column

    def time_slot_clicked(self, button, time, is_selected):
        # Reset the previously selected time slot
        if self.selected_time_slot:
            self.reset_time_slot_color(self.selected_time_slot)

        # Set the new selected time slot
        self.selected_time_slot = time
        print(self.selected_time_slot)

        for row in self.time_slots_column.controls:
            for i, button in enumerate(row.controls):
                # Get the stored text for the button
                button_text = button.content.content.value
                if button_text == time:
                    # Create a new button with the original style and the same text
                    new_button = Container(
                        margin=margin.only(left=10, bottom=5),
                        content=TextButton(
                            content=Text(button_text, size=14, color="#3386C5", font_family="RobotoSlab"),
                            width=95,
                            height=45,
                            style=ButtonStyle(bgcolor={"": colors.WHITE}, shape={"": RoundedRectangleBorder(radius=7)},
                                              side={"": BorderSide(1, "#3386C5")}, ),
                            on_click=lambda control, time_slot=button_text: self.time_slot_clicked(control, time_slot,
                                                                                                   True)
                        )
                    )

                    # Replace the old button with the new one in the time_slots_column controls
                    row.controls[i] = new_button

        # Update your layout to reflect the changes
        self.time_slots_column.update()

        if self.chosen_date:
            current_date = datetime.date.today()
            current_month = current_date.month
            current_year = current_date.year  # Get the current year
            month_name = calendar.month_name[current_month]
            self.appointment_date = f"{self.chosen_date} {month_name} {current_year}"

    def reset_time_slot_color(self, time):
        for row in self.time_slots_column.controls:
            for i, button in enumerate(row.controls):
                # Get the stored text for the button
                button_text = button.content.content.value
                if button_text == time:
                    # Create a new button with the original style and the same text
                    new_button = Container(
                        margin=margin.only(left=10, bottom=5),
                        content=TextButton(
                            content=Text(button_text, size=14, color=colors.WHITE, font_family="RobotoSlab"),
                            width=95,
                            height=45,
                            style=ButtonStyle(bgcolor={"": "#3386C5"}, shape={"": RoundedRectangleBorder(radius=7)}),
                            on_click=lambda control, time_slot=button_text: self.time_slot_clicked(control, time_slot,
                                                                                                   False)
                        )
                    )

                    # Replace the old button with the new one in the time_slots_column controls
                    row.controls[i] = new_button

        # Update your layout to reflect the changes
        self.time_slots_column.update()
        
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Date & Time'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        self.get_timeslots()

        hospital_id = int(params.hospital_id)
        doctor_id = int(params.doctor_id)

        def on_tap(e):

            # print(response.text)

            # if e.control.content.border is None:
            #     e.control.content.border = border.all(10, "blue")
            #     selected_container = e.control
            #     doctor_id = e.control.data
            # else:
            #     e.control.content.border = None
            #     selected_container = None

            e.control.update()

        timeslot = GridView(
            runs_count=3,
            child_aspect_ratio=5/2,
            # spacing=10,
            # padding=10,
        )

        for i in range(len(self.timeslots_data)):
            timestamp = self.timeslots_data[i]['slotDate']  # Unix timestamp
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            time = dt_object.strftime("%I:%M %p")  # Convert to 12-hour clock format

            timeslot.controls.append(
                GestureDetector(
                    on_tap=on_tap,
                    mouse_cursor=MouseCursor.CLICK,
                    content=Container(
                        border_radius=10,
                        alignment=alignment.center,
                        bgcolor=colors.WHITE,
                        content=Text(value=time,
                                     color=colors.GREY_800,
                                     size=12,
                                     ),
                    )
                )
            )

        def go_select_doctor(e):
            page.go(f'/selectDoctor/{hospital_id}')
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Successful"),
            content=Text("Thanks for choosing us."),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(value="Date"),
                            Text(value="Time"),
                            Text(value=f'{svr.get_hospital_name(hospital_id)}'),
                            Text(value=f'{svr.get_doctor_name(doctor_id)}'),
                        ]
                    ))
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        return View(
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    controls=[
                        TextButton(text=f'{svr.get_hospital_name(hospital_id)}, {svr.get_doctor_name(doctor_id)}',
                                   style=ButtonStyle(color=colors.WHITE),
                                   icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color="white",
                                   on_click=go_select_doctor),

                        Row(
                            expand=True,
                            controls=[
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        self.generate_calendar(page),
                                    ]
                                ),
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    controls=[
                                        Container(
                                            height=300,
                                            content=timeslot,
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


                # Row(
                #     alignment=MainAxisAlignment.SPACE_BETWEEN,
                #     controls=[
                #         Column(
                #             expand=True,
                #             horizontal_alignment=CrossAxisAlignment.END,
                #             controls=[
                #                 ElevatedButton(text='Confirm Appointment', on_click=open_dlg_modal),
                #             ]
                #         ),
                #     ],
                # )
            ],
        )
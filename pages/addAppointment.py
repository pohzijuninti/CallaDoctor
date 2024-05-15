import flet as ft
from flet import *
from flet_route import Params, Basket
import datetime


class AddAppointment:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Add Appointment'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        hospital = GridView(
            max_extent=200,
            spacing=10,
            padding=10,
        )

        doctor = GridView(
            max_extent=150,
            spacing=10,
            padding=10,
        )

        for i in range(10):  # range(-1)
            hospital.controls.append(
                Container(
                    border_radius=10,
                    bgcolor="white",
                    width=300,
                    height=300,
                    content=Image(src=f'pantai.png'),  # {i}
                ),
            )

        for i in range(1):  # range(-1)
            doctor.controls.append(
                Container(
                    border_radius=10,
                    bgcolor="white",
                    width=300,
                    height=500,
                    content=Column(
                        alignment=MainAxisAlignment.SPACE_EVENLY,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Image(src=f'drlim.png', width=100, height=100),  # {i}
                            Text(value="Doctor", color='black'),
                        ]
                    )
                )
            )

        return View(
            route="/addAppointment",
            padding=80,
            controls=[
                Row(
                    expand=True,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Select Hospital', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    bgcolor="yellow",
                                    content=hospital
                                ),
                            ]
                        ),
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Select Doctor', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    bgcolor="blue",
                                    content=doctor
                                ),
                            ]
                        ),
                    ]
                ),
                Row(
                    expand=True,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Select Date',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    bgcolor="yellow",
                                ),
                            ]
                        ),
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Select Time',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    bgcolor="blue",
                                ),
                            ]
                        ),
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=True,
                            horizontal_alignment=CrossAxisAlignment.START,
                            controls=[
                                TextField(icon=icons.UPLOAD_FILE_OUTLINED, label='Medical Record',
                                          border=InputBorder.UNDERLINE, disabled=True),
                                ElevatedButton(text='Browse Files'),
                            ]
                        ),
                        Column(
                            expand=True,
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                ElevatedButton(text='Confirm Appointment')
                            ]
                        ),
                    ],
                )
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent
from db.config import register, login
from time import sleep


class Home:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

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
                                        bgcolor="pink",
                                        content=Text('NavBar')
                                    )
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

                                ListView(
                                    auto_scroll=True,
                                    expand=True,
                                    controls=[
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=125,
                                                # here
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
                                                                                Icon(name=icons.DATE_RANGE_OUTLINED,
                                                                                     color="white"),
                                                                                Text(value="Date", color="white")
                                                                            ]
                                                                        ),
                                                                    ),
                                                                    Container(
                                                                        expand=True,
                                                                        content=Row(
                                                                            expand=True,
                                                                            alignment=MainAxisAlignment.START,
                                                                            controls=[
                                                                                Icon(name=icons.ACCESS_TIME_OUTLINED,
                                                                                     color="white"),
                                                                                Text(value="Time", color="white")
                                                                            ]
                                                                        )
                                                                    ),
                                                                    Container(
                                                                        expand=True,
                                                                        content=Row(
                                                                            expand=True,
                                                                            alignment=MainAxisAlignment.START,
                                                                            controls=[
                                                                                Icon(name=icons.LOCAL_HOSPITAL_OUTLINED,
                                                                                     color="white"),
                                                                                Text(value="Hospital", color="white")
                                                                            ]
                                                                        )
                                                                    ),
                                                                    Container(
                                                                        expand=True,
                                                                        content=Row(
                                                                            expand=True,
                                                                            alignment=MainAxisAlignment.START,
                                                                            controls=[
                                                                                Icon(name=icons.PEOPLE_OUTLINED,
                                                                                     color="white"),
                                                                                Text(value="Doctor", color="white")
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
                                                                    IconButton(icon=icons.DELETE_OUTLINED, icon_size=40,
                                                                               icon_color="white"),
                                                                    TextButton(text="Delete",
                                                                               style=ButtonStyle(color=colors.WHITE))
                                                                ]
                                                            )
                                                        )
                                                    ]
                                                ),
                                            ),
                                        ),
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=125,
                                                content=Text('Appointment'),
                                            ),
                                        ),
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=125,
                                                content=Text('Appointment'),
                                            ),
                                        ),
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=125,
                                                content=Text('Appointment'),
                                            ),
                                        ),
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=100,
                                                content=Text('Appointment'),
                                            ),
                                        ),
                                        Container(
                                            padding=5,
                                            content=Container(
                                                border_radius=10,
                                                bgcolor="amber",
                                                width=400,
                                                height=125,
                                                content=Text('Appointment'),
                                            ),
                                        ),
                                    ]
                                ),
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
                                                    content=Text('Calendar'),
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
                                                                bgcolor="green",
                                                                width=145,
                                                                height=100,
                                                                content=Text('Booking History'),
                                                            ),
                                                        ]
                                                    ),
                                                    Column(
                                                        controls=[
                                                            Container(
                                                                expand=True,
                                                                border_radius=10,
                                                                bgcolor="blue",
                                                                width=145,
                                                                height=100,
                                                                content=Text('Graph'),
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
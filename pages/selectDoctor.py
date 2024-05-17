import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as server
from pages.server import get_specialty_name


class SelectDoctor:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

        def go_select_datetime(e):
            page.go("/selectDateTime")
            page.update()

        doctor = GridView(
            max_extent=500,
            spacing=30,
            padding=30,
        )

        for i in range(len(server.doctorList)):
            doctor.controls.append(
                Container(
                    border_radius=10,
                    bgcolor="white",
                    width=300,
                    height=300,
                    content=Column(
                        alignment=MainAxisAlignment.SPACE_EVENLY,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Image(src=f'{server.doctorList[i]["image"]}', width=400, height=250),  # {i}
                            Text(value=f'{server.doctorList[i]["name"]}', color='black', size=25),
                            Text(value=f'{get_specialty_name(server.doctorList[i]["specialityID"])}', color='black', size=20),
                        ]
                    )
                ),
            )

        return View(
            route="/selectDoctor",
            padding=50,
            spacing=50,
            controls=[
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        TextButton(text="Pantai Hospital", style=ButtonStyle(color=colors.WHITE),
                                   icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color="white",
                                   on_click=go_select_hospital)
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
                                    content=Text(value='Select Doctor',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    content=doctor
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
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                TextButton(text="Next", style=ButtonStyle(color=colors.WHITE),
                                           icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color="white",
                                           on_click=go_select_datetime)
                            ]
                        ),
                    ],
                )
            ]
        )
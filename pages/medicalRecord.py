import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr


class MedicalRecord:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        def go_home(e):
            page.go("/home")
            page.update()

        return View(
            route="/medicalRecord",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.WHITE,
                                    on_click=go_home,
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        Container(
                            expand=1,
                            width=300,
                            border_radius=10,
                            bgcolor="white",
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    Row(
                                        expand=2,
                                        alignment=MainAxisAlignment.SPACE_AROUND,
                                        controls=[
                                            Column(
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    Image(src='user.png', width=75, height=100)
                                                ]
                                            ),
                                            Column(
                                                alignment=MainAxisAlignment.CENTER,
                                                controls=[
                                                    Text("Poh Zi Jun", style=TextStyle(color=colors.BLACK)),
                                                    Text("Male", style=TextStyle(color=colors.BLACK)),
                                                    Text("24 years old", style=TextStyle(color=colors.BLACK)),
                                                ]
                                            ),
                                        ]
                                    ),
                                    Row(
                                        expand=1,
                                        alignment=MainAxisAlignment.CENTER,
                                        controls=[
                                            Text(f'{svr.descriptionList[0]["caution"]}',
                                                 style=TextStyle(color=colors.BLACK))
                                        ]
                                    ),
                                ]
                            )
                        ),
                        Container(
                            expand=2,
                            width=300,
                            border_radius=10,
                            bgcolor="white",
                            content=ListView(
                                padding=10,
                                spacing=20,
                                controls=[
                                    Text(value=f'{svr.descriptionList[0]["datetime"]}', style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                    Text(value=f'{svr.descriptionList[0]["description"]}',
                                         style=TextStyle(color=colors.BLACK)),
                                ]
                            )
                        )
                    ]
                ),
            ]
        )

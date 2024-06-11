import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr


class ClinicForm:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Clinic Form'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        def go_login(e):
            page.go("/")
            page.update()

        name: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Hospital Name', border=InputBorder.UNDERLINE, color=colors.BLACK)
        address: TextField = TextField(icon=icons.LOCAL_HOSPITAL_OUTLINED, label='Address', border=InputBorder.UNDERLINE, color=colors.BLACK)
        phone_number: TextField = TextField(icon=icons.LOCAL_PHONE_OUTLINED, label='Phone Number', border=InputBorder.UNDERLINE, color=colors.BLACK)
        email: TextField = TextField(icon=icons.EMAIL_OUTLINED, label='Email', border=InputBorder.UNDERLINE, color=colors.BLACK)
        website: TextField = TextField(icon=icons.INSERT_LINK_OUTLINED, label='Website', border=InputBorder.UNDERLINE, color=colors.BLACK)

        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(text="Submit", style=ButtonStyle(color=colors.WHITE),
                                       icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.WHITE,
                                       #on_click=
                            )
                        ]
                    ),
                ],
            )

        return View(
            route="/clinicForm",
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
                                    on_click=go_login,
                                ),
                                Text(value='Clinic Form', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        Container(
                            expand=True,
                            bgcolor=colors.WHITE,
                            border_radius=10,
                            content=GridView(
                                child_aspect_ratio=10,
                                padding=10,
                                controls=[
                                    name,
                                    address,
                                    phone_number,
                                    email,
                                    website
                                ]
                            )
                        ),
                        display_button(),
                    ]
                ),
            ]
        )

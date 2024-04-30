import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent


class LoginPage:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Login Page'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.DARK
        # page.window_full_screen = True
        page.window_resizable = True

        # Setup fields
        img: Image = Image(src=f"/Users/ameliadavid/Desktop/login.png", width=350, height=350) # 90CFF9
        username: TextField = TextField(icon=ft.icons.SHORT_TEXT_OUTLINED, label='Username', text_align=ft.TextAlign.LEFT, width=200, border=ft.InputBorder.UNDERLINE)
        password: TextField = TextField(icon=ft.icons.LOCK_OUTLINED, label='Password', text_align=ft.TextAlign.LEFT, width=200, border=ft.InputBorder.UNDERLINE, password=True, can_reveal_password=True)
        login: ElevatedButton = ElevatedButton(text='Login', width=200, disabled=True)

        def validate(e: ControlEvent):
            if all([username.value, password.value]):
                login.disabled = False
            else:
                login.disabled = True

            page.update()

        def loginToHome(e: ControlEvent):
            page.go("/homePage")

        username.on_change = validate
        password.on_change = validate
        login.on_click = loginToHome

        return View(
            "/",
            [
                Container(
                    Row(
                        [
                            img,
                            Column(
                                [
                                    Text('Welcome to Call A Doctor! '),
                                    username,
                                    password,
                                    login
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=50
                    ),
                    expand=True,
                )
            ]
        )

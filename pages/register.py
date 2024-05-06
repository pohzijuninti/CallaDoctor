import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent

class Register:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Login'
        page.theme_mode = ft.ThemeMode.DARK

        # Setup fields
        img: Image = Image(src=f'login.png', width=350, height=350) # 90CFF9
        username: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Username', width=200, border=InputBorder.UNDERLINE)
        password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', width=200, border=InputBorder.UNDERLINE,
                                        password=True, can_reveal_password=True)
        login: ElevatedButton = ElevatedButton(text='Login', width=200, disabled=True)
        signup: TextButton = TextButton(text='Create new account', width=200)

        def validate(e: ControlEvent):
            if all([username.value, password.value]):
                login.disabled = False
            else:
                login.disabled = True
            page.update()

        def loginToHome(e: ControlEvent):
            print(username.value)
            print(password.value)
            page.go("/home")

        username.on_change = validate
        password.on_change = validate
        login.on_click = loginToHome

        return View(
            route="/",
            controls = [
                Container(
                    Row(
                        controls = [img,
                                    Column(
                                        controls = [
                                            Text('Welcome to Call A Doctor! '),
                                            username,
                                            password,
                                            login,
                                            signup],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                alignment=MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=50
                    ),
                    expand=True,
                )
            ]
        )

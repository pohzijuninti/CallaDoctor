import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent
from db.config import Signup

class Login:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Login'

        page.window_min_width = 800
        page.window_min_height = 400
        page.window_resizable = True
        page.theme_mode = ft.ThemeMode.DARK

        # Setup fields
        img: Image = Image(src=f'login.png', width=350, height=350) # 90CFF9
        email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', width=250, border=InputBorder.UNDERLINE, text_size=14)
        password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', width=250, border=InputBorder.UNDERLINE, text_size=14,
                                        password=True, can_reveal_password=True)
        login: ElevatedButton = ElevatedButton(text='Login', width=250, disabled=True)
        new_email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', border=InputBorder.UNDERLINE, text_size=14)
        new_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', border=InputBorder.UNDERLINE, text_size=14,
                                        password=True, can_reveal_password=True)

        def close_dlg(e):
            dlg_modal.open = False
            new_email.value = ''
            new_password.value = ''
            page.update()

        def signup(e):
            dlg_modal.open = False
            Signup(new_email.value, new_password.value)
            new_email.value = ''
            new_password.value = ''
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Sign Up"),
            content=Text("It's quick and easy."),
            actions=[
                Container(
                    content=
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[new_email,
                              new_password,
                              Container(padding=padding.only(top=20, bottom=10),content=ElevatedButton(text="Sign Up", on_click=signup, width=250))]
                ))
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def validate(e: ControlEvent):
            if all([email.value, password.value]):
                login.disabled = False
            else:
                login.disabled = True
            page.update()

        def loginToHome(e: ControlEvent):
            print(email.value)
            print(password.value)
            page.go("/home")

        email.on_change = validate
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
                                            email,
                                            password,
                                            login,
                                            TextButton(text='Create new account', width=250, on_click=open_dlg_modal)],
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                alignment=MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=MainAxisAlignment.SPACE_EVENLY,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        spacing=50
                    ),
                    expand=True,
                )
            ]
        )


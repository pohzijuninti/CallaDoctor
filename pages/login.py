import flet as ft
from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent
from db.config import register, login
from time import sleep

class Login:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Login'
        page.window_min_width = 800
        page.window_min_height = 630
        page.window_resizable = True
        page.theme = Theme(
            tabs_theme = TabsTheme(
                indicator_tab_size=True,
            )
        )

        def temp_go_home(e):
            page.go("/home")
            page.update()

        # Setup fields
        img: Image = Image(src=f'login.png', width=350, height=350) # 90CFF9
        email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', width=250, border=InputBorder.UNDERLINE, text_size=14)
        password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', width=250, border=InputBorder.UNDERLINE, text_size=14,
                                        password=True, can_reveal_password=True)
        login_button: ElevatedButton = ElevatedButton(text='Login', width=250, disabled=True)
        new_email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', border=InputBorder.UNDERLINE, text_size=14)
        new_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', border=InputBorder.UNDERLINE, text_size=14,
                                        password=True, can_reveal_password=True)
        temp_button: TextButton = TextButton(text='Temp Home', on_click=temp_go_home)
        tabs: Tabs = Tabs(
                    height=100,
                    width=165,
                    selected_index=0,
                    animation_duration=400,
                    tabs=[
                        Tab(
                            tab_content=Icon(icons.PERSON),
                            content=Container(
                                content=Text(value='User', size=14,
                                             text_align=TextAlign.CENTER),
                            )
                        ),
                        Tab(
                            tab_content=Icon(icons.HEALTH_AND_SAFETY),
                            content=Container(
                                content=Text(value='Doctor', size=14, text_align=TextAlign.CENTER),
                            )
                        ),
                        Tab(
                            tab_content=Icon(icons.ADMIN_PANEL_SETTINGS_OUTLINED),
                            content=Container(
                                content=Text(value='Admin', size=14, text_align=TextAlign.CENTER),
                            )
                        ),
                                                ]
                                            )

        def close_dlg(e):
            dlg_modal.open = False
            new_email.value = ''
            new_password.value = ''
            page.update()

        def signup(e):
            dlg_modal.open = False
            register(new_email.value, new_password.value)
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
                login_button.disabled = False
            else:
                login_button.disabled = True
            page.update()

        def loginToHome(e: ControlEvent):
            if login(email.value, password.value):
                page.go("/home")


        email.on_change = validate
        password.on_change = validate
        login_button.on_click = loginToHome

        return View(
            route="/",
            controls=[
                Container(
                    Row(
                        controls=[
                                    Column(
                                        alignment=MainAxisAlignment.CENTER,
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        expand=True,
                                        controls=[
                                            img,
                                        ]
                                    ),
                                    Column(
                                        expand=True,
                                        controls=[
                                            tabs,
                                            Text(value='Welcome to Call A Doctor! ',
                                                 style=TextStyle(size=18)),
                                            email,
                                            password,
                                            login_button,
                                            TextButton(text='Create new account', width=250, on_click=open_dlg_modal),
                                            TextButton(text='Join us', width=250, on_click=open_dlg_modal),
                                            # temp_button,
                                        ],
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


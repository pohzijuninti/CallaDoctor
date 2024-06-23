from flet import *
from flet_route import Params, Basket
from flet_core.control_event import ControlEvent
from db.config import login
import requests
import json

# Initialize global variable
selected_index = None


class Login:
    def __init__(self):
        pass

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Login'
        page.window_min_width = 900
        page.window_min_height = 630
        page.window_width = 900
        page.window_resizable = True
        page.theme = Theme(
            tabs_theme=TabsTheme(
                indicator_tab_size=True,
            )
        )

        # Function for admin login
        def admin_login():
            try:
                url = "http://localhost:3000/login/admin"

                payload = f'email={email.value}&password={password.value}'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                hospital_id = json.loads(response.text)['hospitalID']

                # Redirect to admin home page
                page.go(f'/adminHome/{hospital_id}')
                page.update()
            except: # Show error dialog if login fails
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()

        # Function for doctor login
        def doctor_login():
            try:
                url = "http://localhost:3000/login/doctor"

                payload = f'email={email.value}&password={password.value}'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(json.loads(response.text))

                doctor_id = json.loads(response.text)['doctorID']

                # Redirect to doctor home page
                page.go(f'/doctorHome/{doctor_id}')
                page.update()
            except:  # Show error dialog if login fails
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()

        # Setup fields
        img: Image = Image(src=f'login.png', width=350, height=350) # 90CFF9
        email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', width=250, border=InputBorder.UNDERLINE, text_size=14)
        password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', width=250, border=InputBorder.UNDERLINE, text_size=14,
                                        password=True, can_reveal_password=True)
        login_button: ElevatedButton = ElevatedButton(text='Login', width=250, disabled=True)
        tabs: Tabs = Tabs(
            height=100,
            width=165,
            selected_index=selected_index,
            animation_duration=400,
            tabs=[
                Tab(
                    tab_content=Icon(icons.PERSON),
                    content=Container(
                        content=Text(value='User', size=14, text_align=TextAlign.CENTER),
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

        # Dialog for displaying login error
        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Error", text_align=TextAlign.CENTER),
            content=Text("Invalid email or password.", text_align=TextAlign.CENTER),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                text='Close', width=150,
                                on_click=lambda e: (setattr(dlg_modal, 'open', False), page.update())
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Validate login form fields
        def validate(e: ControlEvent):
            if all([email.value, password.value]):
                login_button.disabled = False
            else:
                login_button.disabled = True
            page.update()

        # Perform login based on selected tab
        def all_login(e: ControlEvent):
            global selected_index
            if selected_index is None or selected_index == 0:
                if login(email.value, password.value):
                    page.go('/home')
                else:
                    page.dialog = dlg_modal
                    dlg_modal.open = True
                    page.update()
            elif selected_index == 1:
                doctor_login()
            else:
                admin_login()

        # Handle tab change events
        def on_change(e: ControlEvent):
            global selected_index
            if int(e.data) == 0:
                selected_index = 0
            elif int(e.data) == 1:
                selected_index = 1
            else:
                selected_index = 2

        # Navigate to registration page
        def go_register(e):
            page.go("/register")
            page.update()

        # Navigate to clinic form page
        def go_clinic_form(e):
            page.go("/clinicForm")
            page.update()

        # Assign event handlers to UI elements
        email.on_change = validate
        password.on_change = validate
        login_button.on_click = all_login
        tabs.on_change = on_change

        return View(
            bgcolor=colors.GREY_200,
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
                                            Text(value='Welcome to Call A Doctor! ', style=TextStyle(size=18)),
                                            email,
                                            password,
                                            login_button,
                                            TextButton(text='Create new account', width=250, on_click=go_register),
                                            TextButton(text='Join us', width=250, on_click=go_clinic_form),
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


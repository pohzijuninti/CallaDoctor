from flet import *
from flet_route import Params, Basket
from db.config import register


class Register:
    def __init__(self):
        pass

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Register'
        page.window_min_width = 900
        page.window_min_height = 630
        page.window_width = 900
        page.window_resizable = True

        # Setup fields
        new_name: TextField = TextField(icon=icons.PERSON, label='Name', border=InputBorder.UNDERLINE, text_size=14)
        new_ic: TextField = TextField(icon=icons.CREDIT_CARD, label='IC', border=InputBorder.UNDERLINE, text_size=14)
        new_email: TextField = TextField(icon=icons.SHORT_TEXT_OUTLINED, label='Email', border=InputBorder.UNDERLINE, text_size=14)
        new_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', border=InputBorder.UNDERLINE,
                                            text_size=14, password=True, can_reveal_password=True)
        confirm_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Confirm Password', border=InputBorder.UNDERLINE,
                                                text_size=14, password=True, can_reveal_password=True)

        # Function to handle the signup process
        def signup(e):
            if new_name.value == '' or new_ic.value == '' or new_email.value == '' or new_password.value == '':
                open_empty_dlg(e)
            elif new_password.value != confirm_password.value:
                open_error_dlg(e)
            else:
                # Perform registration using provided data
                register(new_email.value, confirm_password.value, new_name.value, new_ic.value)
                open_successful_dlg(e)
                go_login(e)

        # Opens a dialog when the registration form fields are not filled up
        def open_empty_dlg(e):
            page.dialog = empty_dlg_modal
            empty_dlg_modal.open = True
            page.update()

        empty_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Error", text_align=TextAlign.CENTER),
            content=Text("Please fill up the form.", text_align=TextAlign.CENTER),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                text='Close', width=150,
                                on_click=lambda e: (setattr(empty_dlg_modal, 'open', False), page.update())
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Opens a dialog when passwords do not match during registration
        def open_error_dlg(e):
            page.dialog = error_dlg_modal
            error_dlg_modal.open = True
            page.update()

        error_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Error", text_align=TextAlign.CENTER),
            content=Text("Passwords do not match.", text_align=TextAlign.CENTER),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                text='Close', width=150,
                                on_click=lambda e: (setattr(error_dlg_modal, 'open', False), page.update())
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Opens a dialog when registration is successful
        def open_successful_dlg(e):
            page.dialog = successful_dlg_modal
            successful_dlg_modal.open = True
            page.update()

        successful_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Successful Registration", text_align=TextAlign.CENTER),
            content=Text("Thank you! You have successfully registered.", text_align=TextAlign.CENTER),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextButton(
                                text='Close', width=150,
                                on_click=lambda e: (setattr(successful_dlg_modal, 'open', False), page.update())
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Navigate to login page
        def go_login(e):
            page.go("/")
            page.update()

        return View(
            bgcolor=colors.WHITE,
            route="/register",
            controls=[
                Container(
                    Row(
                        controls=[
                            Container(
                                content=Column(
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Row(
                                            controls=[
                                                IconButton(
                                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                                    icon_color=colors.BLACK,
                                                    on_click=go_login,
                                                ),
                                                Text(value='Welcome to Call A Doctor! ', style=TextStyle(size=18)),
                                            ]
                                        ),
                                        new_name,
                                        new_ic,
                                        new_email,
                                        new_password,
                                        confirm_password,
                                        Container(
                                            padding=padding.only(top=20, bottom=10),
                                            content=ElevatedButton(text="Sign Up", on_click=signup, width=250)
                                        )
                                    ]
                                )
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

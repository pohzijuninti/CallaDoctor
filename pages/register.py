from flet import *
from flet_route import Params, Basket
from db.config import register


class Register:
    def __init__(self):
        pass

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
        new_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Password', border=InputBorder.UNDERLINE, text_size=14,
                                            password=True, can_reveal_password=True)
        confirm_password: TextField = TextField(icon=icons.LOCK_OUTLINED, label='Confirm Password', border=InputBorder.UNDERLINE,
                                            text_size=14,
                                            password=True, can_reveal_password=True)


        def signup(e):
            if new_name.value == '' or new_ic.value == '' or new_email.value == '' or new_password.value == '':
                title = 'Error'
                message = 'Please fill up the form.'

            elif new_password.value != confirm_password.value:
                title = 'Error'
                message = 'Passwords do not match.'
            else:
                register(new_email.value, confirm_password.value, new_name.value, new_ic.value)
                title = 'Successful Registration'
                message = 'Thank you! You have successfully registered.'

            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

            # if new_password.value == confirm_password.value:
            #     dlg_modal.open = False
            #     register(new_email.value, confirm_password.value, new_name.value, new_ic.value)
            #     new_name.value = ''
            #     new_ic.value = ''
            #     new_email.value = ''
            #     new_password.value = ''
            #     confirm_password.value = ''
            #     page.go('/')
            #     page.update()
            # else:
            #     page.dialog = dlg_modal
            #     dlg_modal.open = True
            #     page.update()




        if new_name.value == '' or new_ic.value == '' or new_email.value == '' or new_password.value == '':
            title = 'Error'
            message = 'Please fill up the form.'
        elif new_password.value != confirm_password.value:
            title = 'Error'
            message = 'Passwords do not match.'
        else:
            register(new_email.value, confirm_password.value, new_name.value, new_ic.value)
            title = 'Successful Registration'
            message = 'Thank you! You have successfully registered.'

        dlg_modal = AlertDialog(
            modal=False,
            title=Text(title, text_align=TextAlign.CENTER),
            content=Text(message, text_align=TextAlign.CENTER),
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

        def go_login(e):
            page.go("/")
            page.update()

        return View(
            bgcolor=colors.GREY_200,
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


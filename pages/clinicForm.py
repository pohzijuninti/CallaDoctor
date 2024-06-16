import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json

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

        name: TextField = TextField(icon=icons.LOCAL_HOSPITAL_OUTLINED, label='Hospital Name', border=InputBorder.UNDERLINE, color=colors.WHITE)
        address: TextField = TextField(icon=icons.LOCATION_ON_OUTLINED, label='Address', border=InputBorder.UNDERLINE, color=colors.WHITE)
        phone_number: TextField = TextField(icon=icons.LOCAL_PHONE_OUTLINED, label='Phone Number', border=InputBorder.UNDERLINE, color=colors.WHITE)
        email: TextField = TextField(icon=icons.EMAIL_OUTLINED, label='Email', border=InputBorder.UNDERLINE, color=colors.WHITE)

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Thank You", text_align=TextAlign.CENTER),
            content=Text("We have received your application and will get back to you soon."),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text('Your code is #200'),
                            Text(f'Hospital Name: '),
                            Text(f'Hospital Address: '),
                            Text(f'Phone Number: '),
                            Text(f'Email: '),
                            Container(padding=padding.only(top=20, bottom=10),
                                      content=ElevatedButton(text="Back to Login", width=250, on_click=go_login))
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        def open_dlg_modal(e):

            url = "http://localhost:3000/clinic/form"

            payload = f'hospitalName={name.value}&address={address.value}&phone={phone_number.value}&email={email.value}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            form = json.loads(response.text)

            print(form)


            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(
                                on_click=open_dlg_modal,
                                text="Submit", style=ButtonStyle(color=colors.WHITE),
                                icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.WHITE,
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
                                Text(value='Fill in details', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        Container(
                            expand=True,
                            content=Column(
                                width=800,
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    name,
                                    address,
                                    phone_number,
                                    email,
                                ]
                            )
                        ),
                        display_button(),
                    ]
                ),
            ]
        )

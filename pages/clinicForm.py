import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json


class ClinicForm:
    def __init__(self):
        self.potentialCustomersURL = "http://localhost:3000/potential/customer"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.potentialCustomers = None

    def get_potentialCustomers(self):
        self.response = requests.get(self.potentialCustomersURL, headers=self.headers, data=self.payload)
        self.potentialCustomers = json.loads(self.response.text)

        max_id = -1

        for i in range(len(self.potentialCustomers)):
            if self.potentialCustomers[i]["potentialCustomerID"] > max_id:
                max_id = self.potentialCustomers[i]["potentialCustomerID"]

        return max_id

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

        def open_dlg_modal(e):
            if name.value and address.value and phone_number.value and email.value:
                url = "http://localhost:3000/clinic/form"

                payload = f'hospitalName={name.value}&address={address.value}&phone={phone_number.value}&email={email.value}'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                form = json.loads(response.text)
                print(form)

                id = self.get_potentialCustomers()

                dlg_modal.actions = [
                    Container(
                        content=Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Text(f'Your code is #{id}'),
                                Text(f'{name.value}'),
                                Text(f'{address.value}'),
                                Text(f'{phone_number.value}'),
                                Text(f'{email.value}'),
                                Container(
                                    padding=padding.only(top=20, bottom=10),
                                    content=ElevatedButton(text="Back to Login", width=250, on_click=go_login)
                                )
                            ]
                        )
                    )
                ]

                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()
            else:
                print("Please fill in all fields.")

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Thank You", text_align=TextAlign.CENTER),
            content=Text("We have received your application and will get back to you soon."),
            actions_alignment=MainAxisAlignment.CENTER,
        )

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

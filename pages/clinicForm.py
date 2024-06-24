import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json


class ClinicForm:
    def __init__(self):
        self.page = None
        self.potentialCustomersURL = "http://localhost:3000/potential/customer"
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response = None
        self.potentialCustomers = None

        # Setup fields
        self.name = TextField(
            icon=icons.LOCAL_HOSPITAL_OUTLINED, label='Hospital Name', border=InputBorder.UNDERLINE, color=colors.BLACK
        )
        self.address = TextField(
            icon=icons.LOCATION_ON_OUTLINED, label='Address', border=InputBorder.UNDERLINE, color=colors.BLACK
        )
        self.phone_number = TextField(
            icon=icons.LOCAL_PHONE_OUTLINED, label='Phone Number', border=InputBorder.UNDERLINE, color=colors.BLACK
            )
        self.email = TextField(
            icon=icons.EMAIL_OUTLINED, label='Email', border=InputBorder.UNDERLINE, color=colors.BLACK
        )

    # Fetch potential customers from backend
    def get_potentialCustomers(self):
        try:
            self.response = requests.get(self.potentialCustomersURL, headers=self.headers, data=self.payload)
            self.response.raise_for_status()  # Raise an exception for HTTP errors
            self.potentialCustomers = self.response.json()  # Use .json() method to directly get JSON data

            max_id = -1

            # Find the maximum potentialCustomerID
            for customer in self.potentialCustomers:
                if "potentialCustomerID" in customer:
                    if customer["potentialCustomerID"] > max_id:
                        max_id = customer["potentialCustomerID"]
                else:
                    print(f"Missing 'potentialCustomerID' in: {customer}")

            return max_id
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return -1
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return -1

    # Open dialog modal on form submission
    def open_dlg_modal(self, page, e):
        self.page = page

        # Check if all fields are filled
        if self.name.value and self.address.value and self.phone_number.value and self.email.value:
            url = "http://localhost:3000/clinic/form"

            # Prepare payload for POST request
            payload = f'hospitalName={self.name.value}&address={self.address.value}&phone={self.phone_number.value}&email={self.email.value}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            try:
                # Send POST request to submit clinic form
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors
                form = response.json()  # Parse JSON response
                print(form)

                # Get the latest potential customer ID
                id = self.get_potentialCustomers()
                if id == -1:
                    print("Failed to get potential customers.")
                    return

                dlg_modal = AlertDialog(
                    modal=False,
                    title=Text("Thank You", text_align=TextAlign.CENTER),
                    content=Text("We have received your application and will get back to you soon."),
                    actions=[
                        Container(
                            content=Column(
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Text(f'Your code is #{id}'),
                                    Text(f'{self.name.value}'),
                                    Text(f'{self.address.value}'),
                                    Text(f'{self.phone_number.value}'),
                                    Text(f'{self.email.value}'),
                                    Container(
                                        padding=padding.only(top=20, bottom=10),
                                        content=ElevatedButton(text="Back to Login", width=250, on_click=self.go_login)
                                    )
                                ]
                            )
                        )
                    ],
                    actions_alignment=MainAxisAlignment.CENTER,
                )

                self.page.dialog = dlg_modal
                dlg_modal.open = True
                self.page.update()
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
        else:
            print("Please fill in all fields.")

    # Navigate to login page
    def go_login(self, e):
        self.page.go("/")
        self.page.update()

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        self.page = page
        page.title = 'Call a Doctor - Clinic Form'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        # Function to display submit button
        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(
                                on_click=lambda e: self.open_dlg_modal(page, e),
                                text="Submit", style=ButtonStyle(color=colors.BLACK),
                                icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.BLACK,
                            )
                        ]
                    ),
                ],
            )

        return View(
            bgcolor=colors.WHITE,
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
                                    icon_color=colors.BLACK,
                                    on_click=self.go_login,
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
                                    self.name,
                                    self.address,
                                    self.phone_number,
                                    self.email,
                                ]
                            )
                        ),
                        display_button(),
                    ]
                ),
            ]
        )

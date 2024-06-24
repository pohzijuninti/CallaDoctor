import flet as ft
from flet import *
from flet_route import Params, Basket
import requests
import json
import time
import datetime
import pages.server as svr


class DoctorMedicalRecord2:

    def __init__(self):
        self.payload = '='
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.response1 = None
        self.response2 = None
        self.name_card = None
        self.medical_record = None
        self.shared_record = None

    # Fetch user's name card data from server based on user ID
    def get_name_card(self, user_id):
        full_url = f'http://localhost:3000/user/{user_id}'
        self.response1 = requests.get(full_url, headers=self.headers, data=self.payload)
        self.name_card = json.loads(self.response1.text)

    # Fetch medical records of a specific user and doctor from server
    def get_medical_records(self, user_id, doctor_id):
        url = f"http://localhost:3000/medicalRecord/user/doctor/{user_id}/{doctor_id}"
        self.response2 = requests.get(url, headers=self.headers, data=self.payload)
        self.medical_record = json.loads(self.response2.text)

    # Fetch shared medical records between a specific user and doctor from server
    def get_shared_records(self, user_id, doctor_id):
        url = f"http://localhost:3000/shareMedicalRecord/user/doctorID/{user_id}/{doctor_id}"
        response = requests.request("GET", url, headers=self.headers, data=self.payload)
        self.shared_record = json.loads(response.text)

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        doctor_id = int(params.doctor_id)
        user_id = params.user_id

        self.get_name_card(user_id)
        patientName = self.name_card['name']
        page.title = f'{patientName} - Medical Record'

        self.get_medical_records(user_id, doctor_id)
        self.get_shared_records(user_id, doctor_id)

        # Function to navigate to patient list page
        def go_patient_list(hospital_id, doctor_id):
            page.go(f"/doctor/patientList/{hospital_id}/{doctor_id}")
            page.update()

        # Setup fields
        title = TextField(label='Title', width=250, border=InputBorder.UNDERLINE, text_size=14)
        description = TextField(
            label='Description', width=250, border=InputBorder.UNDERLINE, text_size=14,
            multiline=True, min_lines=3, max_lines=3
        )
        caution = TextField(
            label='Caution', width=250, border=InputBorder.UNDERLINE, text_size=14,
            multiline=True, min_lines=3, max_lines=3
        )

        # Open the add medical record dialog modal
        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        # Open the edit caution dialog modal
        def edit_caution(e):
            page.dialog = caution_dlg_modal
            caution_dlg_modal.open = True
            page.update()

        # Close the edit caution dialog and update caution in backend
        def close_caution_dlg(e):
            # Endpoint URL to update user's caution information
            url = "http://localhost:3000/user/caution"
            # Payload data to send in the POST request
            payload = f'userID={user_id}&caution={caution.value}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            # Send a POST request to update user's caution information
            response = requests.request("POST", url, headers=headers, data=payload)

            self.get_name_card(user_id)  # Refresh user's name card data after updating caution
            update_name_card_view()  # Update the view to reflect the updated caution information

            caution_dlg_modal.open = False
            caution.value = ''
            page.update()

        caution_dlg_modal = AlertDialog(
            modal=False,
            title=Text("Edit Caution"),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            caution,
                            Container(
                                padding=padding.only(top=20, bottom=10),
                                content=ElevatedButton(text="Done",
                                                       on_click=close_caution_dlg,
                                                       width=250)
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Close the add medical record dialog and save record in backend
        def close_dlg(e):
            # Get the current UNIX timestamp (epoch time)
            current_unix_time = int(time.time())

            # Endpoint URL to add a new medical record
            url = "http://localhost:3000/medicalRecord/add"
            # Payload data to send in the POST request
            payload = f'datetime={current_unix_time}&title={title.value}&description={description.value}&hospitalID={hospital_id}&doctorID={doctor_id}&userID={user_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # Send a POST request to add the new medical record
            response = requests.request("POST", url, headers=headers, data=payload)

            self.get_medical_records(user_id, doctor_id)  # Refresh medical records data after adding a new record
            update_medical_records_view()  # Update the view to reflect the updated medical records

            dlg_modal.open = False
            title.value = ''
            description.value = ''
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Medical Record"),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            title,
                            description,
                            Container(
                                padding=padding.only(top=20, bottom=10),
                                content=ElevatedButton(text="Done", on_click=close_dlg, width=250)
                            )
                        ]
                    )
                )
            ],
            actions_alignment=MainAxisAlignment.CENTER,
        )

        # Create patient's name card view
        def create_name_card():
            # Determine gender based on the last digit of IC number
            ic_number = self.name_card['ic']

            # Extract digits from ic_number
            digits = ''.join(c for c in ic_number if c.isdigit())

            # Take the first 12 digits
            ic_digits = digits[:12]

            is_odd = int(ic_digits[-1]) % 2 != 0
            gender = "Male" if is_odd else "Female"

            # Calculate user's age based on IC birth year
            current_date = datetime.datetime.now()
            current_year_two_digit = int(str(current_date.year)[-2:])
            current_year = int(str(current_date.year))
            ic_year = int(ic_digits[:2])
            birth_year = 2000 + ic_year if ic_year <= current_year_two_digit else 1900 + ic_year
            age = f"{current_year - birth_year} years old"

            # Display caution message if available
            caution = self.name_card.get('caution', '')
            caution_text = Text(value=f'{caution}', style=TextStyle(color=colors.RED)) if caution else None

            content_controls = [
                Row(
                    controls=[
                        Column(
                            expand=1,
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Icon(icons.PERSON, color=colors.BLACK, size=50),
                            ]
                        ),
                        Column(
                            expand=2,
                            controls=[
                                Text(value=f"{self.name_card['name']}\n{self.name_card['ic']}\n{gender}\n{age}", style=TextStyle(color=colors.BLACK)),
                            ]
                        ),
                    ]
                ),
            ]

            # Add caution text if available
            if caution_text:
                content_controls[0].controls[1].controls.append(caution_text)

            return Container(
                width=300,
                height=150,
                border_radius=10,
                bgcolor="white",
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=content_controls
                )
            )

        # Update the name card view
        def update_name_card_view():
            name_card_container.content = create_name_card()
            page.update()

        shared_records = GridView(
            padding=padding.only(top=10),
            runs_count=3,
            child_aspect_ratio=10 / 9,
        )

        for j in range(len(self.shared_record)):
            shared_records.controls.append(
                Container(
                    border_radius=10,
                    bgcolor='white',
                    content=Container(
                        padding=10,
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Column(
                                    controls=[
                                        Row(
                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                Text(
                                                    value=f'{svr.convert_date(self.shared_record[j]["datetime"])}, 'f'{svr.convert_time(self.shared_record[j]["datetime"])}',
                                                    color=colors.GREY),
                                            ]
                                        ),
                                        Text(value=f'{self.shared_record[j]["title"]}', size=18, color=colors.BLACK, weight=FontWeight.BOLD),
                                        Text(value='Description', color=colors.BLACK),
                                        Text(value=f'{self.shared_record[j]["description"]}', color=colors.GREY),
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        Text(
                                            value=f'{svr.get_hospital_name(self.shared_record[j]["hospitalID"])}\n{svr.get_doctor_name(self.shared_record[j]["doctorID"])}',
                                            color=colors.BLACK, size=12),
                                    ]
                                )
                            ]
                        )
                    )
                )
            )

        medical_records = GridView(
            padding=padding.only(top=10),
            runs_count=3,
            child_aspect_ratio=10 / 9,
        )

        # Delete a medical record
        def delete_medical_record(e):
            record_id = e.control.data  # Get the record ID from the control's data

            # Send a request to delete the medical record with the given record ID
            url = "http://localhost:3000/medicalRecord/delete/"
            payload = f'recordID={record_id}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.request("POST", url, headers=headers, data=payload)

            self.get_medical_records(user_id, doctor_id)  # Refresh medical records data after adding a new record
            update_medical_records_view()  # Update the view to reflect the updated medical records

        # Update the medical records view
        def update_medical_records_view():
            medical_records.controls.clear()
            for i in range(len(self.medical_record)):
                medical_records.controls.append(
                    Container(
                        border_radius=10,
                        bgcolor='white',
                        content=Container(
                            padding=10,
                            content=Column(
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    Column(
                                        controls=[
                                            Row(
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    Text(
                                                        value=f'{svr.convert_date(self.medical_record[i]["datetime"])}, {svr.convert_time(self.medical_record[i]["datetime"])}',
                                                        color=colors.GREY),
                                                    IconButton(
                                                        data=self.medical_record[i]["recordID"],
                                                        icon_color='red',
                                                        icon='delete',
                                                        on_click=delete_medical_record
                                                    )
                                                ]
                                            ),
                                            Text(value=f'{self.medical_record[i]["title"]}', size=18, color=colors.BLACK, weight=FontWeight.BOLD),
                                            Text(value='Description', color=colors.BLACK),
                                            Text(value=f'{self.medical_record[i]["description"]}', color=colors.GREY),
                                        ]
                                    ),
                                    Row(
                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            Text(value=f'{svr.get_hospital_name(self.medical_record[i]["hospitalID"])}\n{svr.get_doctor_name(self.medical_record[i]["doctorID"])}', color=colors.BLACK, size=12),
                                        ]
                                    )
                                ]
                            )
                        )
                    )
                )
            page.update()

        update_medical_records_view()  # Initialize the GridView with current medical records

        name_card_container = Container(content=create_name_card())

        return View(
            bgcolor=colors.GREY_200,
            route='/doctorMedicalRecord2/:hospital_id/:doctor_id/:user_id',
            padding=50,
            spacing=50,
            controls=[
                ListView(
                    expand=True,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.BLACK,
                                    on_click=lambda e: go_patient_list(hospital_id, doctor_id)
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        Row(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=CrossAxisAlignment.START,
                            controls=[
                                name_card_container,
                                Column(
                                    horizontal_alignment=CrossAxisAlignment.END,
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        ElevatedButton(
                                            on_click=open_dlg_modal,
                                            content=Text('Add Medical Record')
                                        ),
                                        ElevatedButton(
                                            on_click=edit_caution,
                                            content=Text('Edit Caution')
                                        ),
                                    ]
                                )
                            ]
                        ),
                        Container(
                            expand=True,
                            content=medical_records,
                        ),
                        Container(
                            expand=True,
                            content=shared_records,
                        ),
                    ]
                ),
            ]
        )

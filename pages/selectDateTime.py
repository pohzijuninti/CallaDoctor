import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr
import datetime


class SelectDateTime:
    def __init__(self):
        pass

    def generate_calendar(self, page):
        current_date = datetime.date.today()
        current_year = current_date.year
        current_month = current_date.month
        
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Date & Time'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        hospital_id = int(params.hospital_id)
        doctor_id = int(params.doctor_id)

        def go_select_doctor(e):
            page.go(f'/selectDoctor/{hospital_id}')
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Successful"),
            content=Text("Thanks for choosing us."),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            Text(value="Date"),
                            Text(value="Time"),
                            Text(value=f'{svr.get_hospital_name(hospital_id)}'),
                            Text(value=f'{svr.get_doctor_name(doctor_id)}'),
                        ]
                    ))
            ],
            actions_alignment=MainAxisAlignment.CENTER,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        def open_dlg_modal(e):
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        return View(
            route="/selectDateTime/:hospital_id:doctor_id",
            padding=50,
            spacing=50,
            controls=[
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        TextButton(text=f'{svr.get_hospital_name(hospital_id)}, {svr.get_doctor_name(doctor_id)}', style=ButtonStyle(color=colors.WHITE),
                                   icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color="white",
                                   on_click=go_select_doctor)
                    ]
                ),
                Row(
                    expand=True,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=2,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    expand=True,
                                    bgcolor="yellow",
                                    # content,
                                ),

                            ]
                        ),
                        Column(
                            expand=1,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    expand=True,
                                    bgcolor="red"
                                )
                            ]
                        )
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=True,
                            horizontal_alignment=CrossAxisAlignment.END,
                            controls=[
                                ElevatedButton(text='Confirm Appointment', on_click=open_dlg_modal),
                            ]
                        ),
                    ],
                )
            ],
        )
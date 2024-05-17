import flet as ft
from flet import *
from flet_route import Params, Basket


class SelectDateTime:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Date & Time'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        def go_select_doctor(e):
            page.go("/selectDoctor")
            page.update()

        dlg_modal = AlertDialog(
            modal=False,
            title=Text("Successful"),
            content=Text("Thanks for choosing us."),
            actions=[
                Container(
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        controls=[Text(value="Date"),
                                  Text(value="Time"),
                                  Text(value="Hospital"),
                                  Text(value="Doctor"),
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
            route="/selectDateTime",
            padding=50,
            spacing=50,
            controls=[
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        TextButton(text="Pantai Hospital, Dr. Lim Guan Choon", style=ButtonStyle(color=colors.WHITE),
                                   icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color="white",
                                   on_click=go_select_doctor)
                    ]
                ),
                Row(
                    expand=True,
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Column(
                            expand=True,
                            alignment=MainAxisAlignment.CENTER,
                            controls=[
                                Container(
                                    padding=padding.only(left=5),
                                    content=Text(value='Select Date & Time',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    bgcolor="yellow",
                                    # content=
                                ),
                            ]
                        ),
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
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr

selected_container = None
doctor_id = None


class SelectDoctor:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        hospital_id = int(params.hospital_id)
        svr.get_doctor_details(hospital_id),

        def go_select_hospital(e):
            global selected_container
            selected_container = None

            page.go("/selectHospital")
            page.update()

        def go_select_datetime(e):
            global selected_container
            selected_container = None

            if doctor_id is not None:
                page.go(f'/selectDateTime/{hospital_id}{doctor_id}')
                page.update()

        def on_tap(e):
            global selected_container
            global doctor_id

            if selected_container is not None and selected_container != e.control:
                selected_container.content.border = None
                selected_container.update()

            if e.control.content.border is None or selected_container != e.control:
                e.control.content.border = border.all(10, colors.BLUE_100)
                selected_container = e.control
                doctor_id = e.control.data
            else:
                e.control.content.border = None
                selected_container = None

            e.control.update()

        doctor = GridView(
            runs_count=3,
            child_aspect_ratio=8/9,
            spacing=30,
            padding=30,
        )

        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(text="Next", style=ButtonStyle(color=colors.WHITE),
                                       icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.WHITE,
                                       on_click=go_select_datetime)
                        ]
                    ),
                ],
            )

        for i in range(len(svr.doctorFilteredList)):
            doctor.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    data=int(svr.doctorFilteredList[i]["doctorID"]),
                    content=Container(
                        border_radius=10,
                        bgcolor="white",
                        content=Container(
                            content=Column(
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                controls=[
                                    Container(
                                        expand=3,
                                        padding=padding.only(top=10),
                                        content=Image(src=f'{svr.doctorFilteredList[i]["image"]}', fit=ImageFit.FIT_HEIGHT),
                                    ),
                                    Column(
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        expand=1,
                                        controls=[
                                            Text(value=f'{svr.doctorFilteredList[i]["name"]}', color='black', size=12),
                                            Text(value=f'{svr.get_speciality_name(svr.doctorFilteredList[i]["specialityID"])}',
                                                 color='black', size=10),
                                        ]
                                    )
                                ]
                            )
                        )
                    ),
                )
            )

        return View(
            route="/selectDoctor/:hospital_id",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                TextButton(
                                    text=f'{svr.get_hospital_name(hospital_id)}',
                                    style=ButtonStyle(color=colors.WHITE),
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color=colors.WHITE,
                                    on_click=go_select_hospital
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=doctor,
                        ),
                        display_button(),
                    ]
                ),
            ]
        )
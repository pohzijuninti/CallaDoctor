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

        def go_select_hospital(e):
            page.go("/selectHospital")
            page.update()

        def go_select_datetime(e):
            page.go(f'/selectDateTime/{hospital_id}{doctor_id}')
            page.update()

        def on_tap(e):
            global selected_container
            global doctor_id

            if selected_container is not None and selected_container != e.control:
                selected_container.content.border = None
                selected_container.update()

            if e.control.content.border is None or selected_container != e.control:
                e.control.content.border = border.all(10, "blue")
                selected_container = e.control
                doctor_id = e.control.data
            else:
                e.control.content.border = None
                selected_container = None

            e.control.update()

        doctor = GridView(
            runs_count=3,
            child_aspect_ratio=10 / 9,
            spacing=30,
            padding=30,
        )

        svr.get_doctor_details(hospital_id)

        for i in range(len(svr.doctorFilteredList)):
            doctor.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    data=int(svr.doctorFilteredList[i]["doctorID"]),
                    content=Container(
                        border_radius=10,
                        bgcolor="white",
                        width=300,
                        height=300,
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Image(src=f'{svr.doctorFilteredList[i]["image"]}', width=400, height=250),
                                Text(value=f'{svr.doctorFilteredList[i]["name"]}', color='black', size=18),
                                Text(value=f'{svr.get_speciality_name(svr.doctorFilteredList[i]["specialityID"])}', color='black', size=15),
                            ]
                        )
                    ),
                )
            )

        return View(
            route="/selectDoctor/:hospital_id",
            padding=50,
            spacing=50,
            controls=[
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        TextButton(text=f'{svr.get_hospital_name(hospital_id)}', style=ButtonStyle(color=colors.WHITE),
                                   icon=icons.ARROW_BACK_IOS_NEW_OUTLINED, icon_color="white",
                                   on_click=go_select_hospital)
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
                                    content=Text(value='Select Doctor',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    content=doctor
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
                                TextButton(text="Next", style=ButtonStyle(color=colors.WHITE),
                                           icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color="white",
                                           on_click=go_select_datetime)
                            ]
                        ),
                    ],
                )
            ]
        )
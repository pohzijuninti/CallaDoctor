import flet as ft
from flet import *
from flet_route import Params, Basket

class PatientList:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Doctor - Patient List'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        doctor_id = int(params.doctor_id)

        def go_doctor_home(e):
            page.go(f'/doctorHome/{doctor_id}')
            page.update()

        patient = ListView(
            expand=True,
            spacing=10,
            padding=20,
        )

        for i in range(10):
            patient.controls.append(
                ListTile(
                    shape=RoundedRectangleBorder(
                        radius=10
                    ),
                    bgcolor='white',
                    leading=Icon(icons.PERSON, size=30),
                    title=Text('Name'),
                    subtitle=Text('ic'),
                    trailing=IconButton(
                        icon=icons.EDIT_DOCUMENT,
                    )
                ),
            )


        return View(
            padding=50,
            spacing=50,
            bgcolor=colors.GREY_200,
            route="/doctor/patientList/:doctor_id",
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.GREY_800,
                                    on_click=go_doctor_home,
                                ),
                                Text(
                                    value='Patient List',
                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                ),
                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=patient
                        ),
                    ]
                )
            ]
        )
import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr

selected_container = None
hospital_id = None


class SelectHospital:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Hospital'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 800
        page.window_min_height = 630

        def go_home(e):
            global selected_container
            selected_container = None

            page.go("/home")
            page.update()

        def go_select_doctor(e):
            if hospital_id is not None:
                page.go(f'/selectDoctor/{hospital_id}')
                page.update()

        # def search_hospital(e):

        def on_tap(e):
            global selected_container
            global hospital_id

            if selected_container is not None and selected_container != e.control:
                selected_container.content.border = None
                selected_container.update()

            if e.control.content.border is None or selected_container != e.control:
                e.control.content.border = border.all(10, colors.BLUE_100)
                selected_container = e.control
                hospital_id = e.control.data
            else:
                e.control.content.border = None
                selected_container = None

            e.control.update()

        hospital = GridView(
            runs_count=3,
            child_aspect_ratio=10/9,
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
                                       on_click=go_select_doctor)
                        ]
                    ),
                ],
            )

        for i in range(len(svr.hospitalList)):
            hospital.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    data=int(svr.hospitalList[i]["hospitalID"]),
                    content=Container(
                        border_radius=10,
                        bgcolor="white",
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Image(src=f'{svr.hospitalList[i]["image"]}', fit=ImageFit.COVER),
                                Text(value=f'{svr.hospitalList[i]["name"]}', color='black', size=12),
                            ]
                         ),
                    ),
                ),
            )

        return View(
            route="/selectHospital",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                Column(
                                    expand=2,
                                    controls=[
                                        Row(
                                            controls=[
                                                IconButton(
                                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                                    icon_color=colors.WHITE,
                                                    on_click=go_home,
                                                ),
                                                Text(value='Select Hospital',
                                                     style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                            ]
                                        ),

                                    ]
                                ),
                                Column(
                                    expand=1,
                                    horizontal_alignment=CrossAxisAlignment.END,
                                    controls=[
                                        IconButton(
                                            icon=icons.SEARCH_OUTLINED,
                                            icon_color=colors.WHITE,
                                            hover_color=colors.BLUE_100,
                                            # on_click=search_hospital,
                                        ),
                                    ]
                                )

                            ]
                        ),
                        Container(
                            expand=True,
                            border_radius=10,
                            content=hospital
                        ),
                        display_button(),
                    ]
                ),
            ]
        )

import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as server


class SelectHospital:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Hospital'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        hospital_id = GestureDetector.data
        # is_tapped = False

        def go_home(e):
            page.go("/home")
            page.update()

        def go_select_doctor(e):
            page.go("/selectDoctor")  # page.go(f'/selectDoctor/{hospital_id}')
            page.update()

        def on_tap(e):
            if e.control.content.border is None:
                print(hospital_id)
                e.control.content.border = border.all(10, "blue")
                e.control.update()
            else:
                e.control.content.border = None
                e.control.update()

        hospital = GridView(
            max_extent=400,
            spacing=30,
            padding=30,
        )

        for i in range(len(server.hospitalList)):
            hospital.controls.append(
                GestureDetector(
                    mouse_cursor=MouseCursor.CLICK,
                    on_tap=on_tap,
                    data=int(server.hospitalList[i]["hospitalID"]),  # wrong
                    content=Container(
                        border_radius=10,
                        bgcolor="white",
                        width=300,
                        height=300,
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Image(src=f'{server.hospitalList[i]["image"]}', width=400, height=250),
                                Text(value=f'{server.hospitalList[i]["name"]}', color='black', size=20),
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
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        ElevatedButton(text='Back to Home', on_click=go_home),
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
                                    content=Text(value='Select Hospital',
                                                 style=TextStyle(size=24, weight=FontWeight.BOLD)),
                                ),
                                Container(
                                    expand=True,
                                    border_radius=10,
                                    content=hospital
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
                                           on_click=go_select_doctor)
                            ]
                        ),
                    ],
                )
            ]
        )
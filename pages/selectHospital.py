import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr

# Initialize global variables
selected_container = None
hospital_id = None


class SelectHospital:
    def __init__(self):
        pass

    # Main view function for the page
    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Select Hospital'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        # Navigate to home page
        def go_home(e):
            global selected_container
            selected_container = None

            page.go("/home")
            page.update()

        # Navigate to hospital info page
        def go_hospital_info(e):
            page.go(f"/hospital/info/{e.control.data}")
            page.update()

        # Navigate to select doctor page
        def go_select_doctor(e):
            global selected_container
            selected_container = None

            if hospital_id is not None:
                page.go(f'/selectDoctor/{hospital_id}')
                page.update()

        # Handle click event on hospital search result
        def on_click(e):
            global hospital_id
            hospital_id = e.control.data
            go_select_doctor(e)

        # Create a search bar with hospital list
        search_bar: SearchBar = SearchBar(
            width=300,
            bar_hint_text='Search...',
            bar_leading=Container(
                padding=10,
                content=Icon(icons.SEARCH_OUTLINED, color=colors.BLACK),
            ),
            controls=[
                ListTile(
                    title=Text(f'{svr.hospitalList[i]["name"]}'), on_click=on_click,
                    data=int(svr.hospitalList[i]["hospitalID"])
                )
                for i in range(len(svr.hospitalList))
            ]
        )

        # Handle tap event on a hospital's card
        def on_tap(e):
            global selected_container
            global hospital_id

            # Deselect previously selected doctor if any
            if selected_container is not None and selected_container != e.control:
                selected_container.content.border = None
                selected_container.update()

            # Toggle selection of the current hospital's card
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

        # Function to display next button
        def display_button():
            return Row(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(
                        expand=True,
                        horizontal_alignment=CrossAxisAlignment.END,
                        controls=[
                            TextButton(
                                text="Next", style=ButtonStyle(color=colors.GREY_800),
                                icon=icons.ARROW_FORWARD_IOS_OUTLINED, icon_color=colors.GREY_800,
                                on_click=go_select_doctor
                            )
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
                        bgcolor=colors.WHITE,
                        content=Column(
                            alignment=MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            controls=[
                                Row(
                                    expand=1,
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        IconButton(
                                            data=int(svr.hospitalList[i]["hospitalID"]),
                                            icon=icons.INFO,
                                            icon_color='grey',
                                            on_click=go_hospital_info
                                        ),
                                    ]
                                ),
                                Image(expand=3, src=f'{svr.hospitalList[i]["image"]}', fit=ImageFit.COVER),
                                Container(
                                    expand=1,
                                    padding=padding.only(top=5),
                                    content=Text(value=f'{svr.hospitalList[i]["name"]}', color=colors.BLACK, size=12, text_align=TextAlign.CENTER),
                                )
                            ]
                        ),
                    ),
                ),
            )

        return View(
            bgcolor=colors.GREY_200,
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
                                                    icon_color=colors.GREY_800,
                                                    on_click=go_home,
                                                ),
                                                Text(
                                                    value='Select Hospital',
                                                    style=TextStyle(size=24, weight=FontWeight.BOLD)
                                                ),
                                            ]
                                        ),

                                    ]
                                ),
                                search_bar,
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

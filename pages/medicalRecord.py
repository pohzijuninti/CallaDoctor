import flet as ft
from flet import *
from flet_route import Params, Basket
import pages.server as svr


class MedicalRecord:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor - Medical Record'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_min_width = 900
        page.window_min_height = 630

        def name_card():
            name = 'Poh Zi Jun'
            gender = 'Male'
            age = '24 years old'
            caution = 'Allergic to Panadol'
            return Container(
                width=300,
                height=150,
                border_radius=10,
                bgcolor="white",
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Row(
                            controls=[
                                Column(
                                    expand=1,
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    controls=[
                                        Icon(icons.PERSON,
                                             color=colors.BLACK,
                                             size=50,
                                             ),
                                    ]
                                ),
                                Column(
                                    expand=2,
                                    controls=[
                                        Text(value=f"{name}\n{gender}\n{age}", style=TextStyle(color=colors.BLACK)),
                                        Text(value=f"**{caution}**", style=TextStyle(color=colors.RED)),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            )

        medical_record = GridView(
            runs_count=3,
            child_aspect_ratio=10 / 9,
            # spacing=30,
            # padding=30,
        )

        for i in range(9):
            medical_record.controls.append(
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
                                        Text(value='15 June 2024, 3:15 PM', color=colors.GREY),
                                        Text(value='Broke His Leg', size=18, color=colors.BLACK,
                                             weight=FontWeight.BOLD),
                                        Text(value='Description', color=colors.BLACK),
                                        Text(value='*Fall down from bike\n*Broke his left leg', color=colors.GREY),
                                    ]
                                ),
                                Row(
                                    alignment=MainAxisAlignment.END,
                                    controls=[
                                        IconButton(icon=icons.SEND, icon_color=colors.BLUE),
                                    ]
                                )

                            ]
                        )
                    )
                )
            )

        def go_home(e):
            page.go("/home")
            page.update()

        return View(
            route="/medicalRecord",
            padding=50,
            spacing=50,
            controls=[
                Column(
                    expand=True,
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(
                            controls=[
                                IconButton(
                                    icon=icons.ARROW_BACK_IOS_NEW_OUTLINED,
                                    icon_color=colors.WHITE,
                                    on_click=go_home,
                                ),
                                Text(value='Medical Record', style=TextStyle(size=24, weight=FontWeight.BOLD)),
                            ]
                        ),
                        name_card(),
                        Container(
                            expand=True,
                            content=medical_record,
                        ),
                        # Container(
                        #     expand=2,
                        #     width=300,
                        #     border_radius=10,
                        #     bgcolor="white",
                        #     content=ListView(
                        #         padding=10,
                        #         spacing=20,
                        #         controls=[
                        #             Text(value=f'{svr.descriptionList[0]["datetime"]}', style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #             Text(value=f'{svr.descriptionList[0]["description"]}',
                        #                  style=TextStyle(color=colors.BLACK)),
                        #         ]
                        #     )
                        # )
                    ]
                ),
            ]
        )

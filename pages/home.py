import flet as ft
from flet import *
from flet_route import Params, Basket

class Home:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.DARK
        # page.window_full_screen = True
        page.window_resizable = True

        return View(
            "/home",
            [
                Container(
                    Row(
                        [
                            TextField(value='Home Page', border=ft.InputBorder.NONE, text_align=ft.TextAlign.CENTER)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                )
            ]
        )

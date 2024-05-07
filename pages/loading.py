import flet as ft
from flet import *

class Loading:
    def __init__(self):
        pass

    def view(self, page: Page):
        page.vertical_alignment = MainAxisAlignment.CENTER
        page.horizontal_alignment = CrossAxisAlignment.CENTER

        return View(
            route="/loading",
            controls=[Text('test')]
        )
import flet as ft
from flet import TextField
from flet_core.control_event import ControlEvent

def main(page: ft.Page) -> None:
    page.title = 'Increment counter'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = 'light'

    text_number: TextField = TextField(value='0',text_align=ft.TextAlign.RIGHT, width=100)

    def decrement(e: ControlEvent) -> None:
        text_number.value = str(int(text_number.value) -1)
        page.update()

    def increment(e: ControlEvent) -> None:
        text_number.value = str(int(text_number.value) +1)
        page.update()

    page.add(
        ft.Row(
            [ft.IconButton(ft.icons.REMOVE, on_click=decrement),
             text_number,
             ft.IconButton(ft.icons.ADD, on_click=increment)
             ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
if __name__ == '__main__':
    ft.app(target=main)
import flet as ft
from flet import *
from flet_route import Routing, path

# Interfaces
from pages.login import LoginPage
from pages.home import HomePage

def main(page: Page):
    page.theme_mode = ft.ThemeMode.DARK

    app_routes = [
        # Interfaces' path
        path(url='/', clear=False, view=LoginPage().view),  # first page url must be '/'
        path(url='/homePage', clear=False, view=HomePage().view),
    ]
    Routing(page=page, app_routes=app_routes)
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
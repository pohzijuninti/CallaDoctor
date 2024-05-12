import flet as ft
from flet import *
from flet_route import Routing, path

# Interfaces
from pages.login import Login
from pages.homeold import HomeOld
from pages.home import Home

def main(page: Page):
    page.theme_mode = ft.ThemeMode.DARK

    app_routes = [
        # Interfaces' path
        path(url='/', clear=False, view=Login().view),  # first page url must be '/'
        path(url='/home', clear=False, view=Home().view),
    ]
    Routing(page=page, app_routes=app_routes)
    page.go(page.route)

if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
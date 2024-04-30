import flet as ft
from flet import *
from flet_route import Routing, path

# Interfaces
from loginPage import LoginPage
from homePage import HomePage


def main(mainPage: Page):
    mainPage.theme_mode = ft.ThemeMode.DARK

    app_routes = [
        # Interfaces' path
        path(url='/', clear=False, view=LoginPage().view),  # first page url must be '/'
        path(url='/homePage', clear=False, view=HomePage().view),
    ]
    Routing(page=mainPage, app_routes=app_routes)
    mainPage.go(mainPage.route)


if __name__ == '__main__':
    ft.app(target=main)
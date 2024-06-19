import flet as ft
from flet import *
from flet_route import Params, Basket
import datetime
import calendar
from calendar import HTMLCalendar
from dateutil import relativedelta
import time


class FletCalendar(ft.UserControl):

    def __init__(self, page):
        super().__init__()

        self.page = page
        self.get_current_date()
        self.set_theme()

        # Init the container control.
        self.calendar_container = ft.Container(width=355, height=300,
                                               padding=ft.padding.all(2),
                                               bgcolor=colors.WHITE,
                                               # border=ft.border.all(2),
                                               border_radius=ft.border_radius.all(10),
                                               alignment=ft.alignment.bottom_center)
        self.build()  # Build the calendar.
        self.output = ft.Text()  # Add output control.

    def get_current_date(self):
        '''Get the initial current date'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year

    def selected_date(self, e):
        '''User selected date'''
        self.output.value = e.control.data
        self.output.update()
        # return e.control.data

    def set_current_date(self):
        '''Set the calendar to the current date.'''
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
        self.build()
        self.calendar_container.update()

    def get_next(self, e):
        '''Move to the next month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current + add_month

        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_prev(self, e):
        '''Move to the previous month.'''
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta.relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_calendar(self):
        '''Get the calendar from the calendar module.'''
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)

    def set_theme(self,
                  text_color=ft.colors.BLACK,
                  current_day_color=ft.colors.RED):
        self.text_color = text_color
        self.current_day_color = current_day_color

    def build(self):
        '''Build the calendar for flet.'''
        current_calendar = self.get_calendar()

        str_date = '{0} {1}'.format(calendar.month_name[self.current_month], self.current_year)

        date_display = ft.Text(str_date, text_align='center', size=20, color=self.text_color, weight=FontWeight.BOLD)
        next_button = ft.Container(ft.Text('>', text_align='right', size=20, color=self.text_color),
                                   on_click=self.get_next)

        prev_button = ft.Container(ft.Text('<', text_align='left', size=20, color=self.text_color),
                                   on_click=self.get_prev)

        calendar_column = ft.Column(
            [ft.Row([prev_button, date_display, next_button], alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER, height=40, expand=False)],
            spacing=2, width=355, height=330, alignment=ft.MainAxisAlignment.START, expand=False)
        # Loop weeks and add row.
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    is_current_day_bg = ft.colors.TRANSPARENT
                    display_day = str(day)
                    if len(str(display_day)) == 1: display_day = '0%s' % display_day
                    if day == self.current_day:
                        is_current_day_font = ft.FontWeight.BOLD
                        is_current_day_bg = self.current_day_color

                    day_button = ft.Container(
                        content=ft.Text(str(display_day), weight=is_current_day_font, color=self.text_color),
                        on_click=self.selected_date, data=(self.current_month, day, self.current_year),
                        width=40, height=40, ink=True, alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(100),
                        bgcolor=is_current_day_bg)
                else:
                    day_button = ft.Container(width=40, height=40, border_radius=ft.border_radius.all(100))

                week_row.controls.append(day_button)

            # Add the weeks to the main column.
            calendar_column.controls.append(week_row)
        # Add column to our page container.
        self.calendar_container.content = calendar_column
        return self.calendar_container

class MordernNavBar(UserControl):
    def __init__(self):
        super().__init__()

    def ContainedIcon(self, icon_name:str, text:str):
        return Container(
            width=180,
            height=45,
            border_radius=10,
            on_hover=lambda e: self.HighLight(e),
            content=Row(
                controls=[
                    IconButton(
                        icon=icon_name,
                        icon_size=18,
                        icon_color='white54',
                        style=ButtonStyle(
                            shape={
                                "":RoundedRectangleBorder(radius=7),
                            },
                            overlay_color={
                                "":"transparent"
                            },
                        ),
                    ),
                    Text(
                        value=text,
                        color="white54",
                        size=11,
                        opacity=1,
                        animate_opacity=200,
                    )
                ]
            ),
        )

    def HighLight(self, e):
        if e.data == 'true':
            e.control.bgcolor = 'white10'
            e.control.update()
            e.control.content.controls[0].icon_color = 'white'
            e.control.content.controls[1].color = 'white'
            e.control.content.update()
        else:
            e.control.bgcolor = None
            e.control.update()
            e.control.content.controls[0].icon_color = 'white54'
            e.control.content.controls[1].color = 'white54'
            e.control.content.update()

    def UserData(self, initials: str, name: str, description: str):

        return Container(
            content=Row(
                controls=[
                    Container(
                        width=42,
                        height=42,
                        bgcolor='bluegrey900',
                        alignment=alignment.center,
                        border_radius=8,
                        content=Text(
                            value=initials,
                            size=20,
                            weight="bold",
                        ),
                    ),
                    Column(
                        spacing=1,
                        alignment='center',
                        controls=[
                            Text(
                                value=name,
                                size=11,
                                weight='bold',
                                opacity=1,
                                animate_opacity=200
                            ),
                            Text(
                                value=description,
                                size=9,
                                weight='w400',
                                color='white54',
                                opacity=1,
                                animate_opacity=200
                            ),
                        ]
                    )
                ]
            )
        )
        pass



    def build(self):
        return Container(
            width=200,
            height=580,
            padding=padding.only(top=10),
            alignment=alignment.center,
            content=Column(
                controls=[
                    self.UserData(initials='ZJ', name='Poh Zi Jun', description='Software Engineer'),
                    Divider(height=5, color="transparent"),
                    self.ContainedIcon(icons.SEARCH, text="Search"),
                    self.ContainedIcon(icons.DASHBOARD_ROUNDED, text="DashBoard"),
                    self.ContainedIcon(icons.BAR_CHART, text="Revenue"),
                    self.ContainedIcon(icons.NOTIFICATIONS, text="Notifications"),
                    self.ContainedIcon(icons.PIE_CHART_ROUNDED, text="Analytics"),
                    self.ContainedIcon(icons.FAVORITE_ROUNDED, text="Likes"),
                    self.ContainedIcon(icons.WALLET_ROUNDED, text="Wallet"),
                    Divider(height=5, color="white24"),
                    self.ContainedIcon(icons.LOGOUT_ROUNDED, text="Logout"),
                ]
            )
        )

class HomeOld:
    def __init__(self):
        pass

    def view(self, page: Page, params: Params, basket: Basket):
        page.title = 'Call a Doctor'
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.window_full_screen = True
        page.window_min_width = 1050
        page.window_min_height = 600

        def logout(e):
            page.route = "/"
            page.update()

        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")

        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")

        date_picker = DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        mycal = FletCalendar(page)

        page.overlay.append(date_picker)

        date_button = ft.ElevatedButton(
            "Make Appointment",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda _: date_picker.pick_date(),
        )

        return View(
            route="/homeold",
            controls=[
                Row(
                    expand=True,
                    controls=[
                        Container(
                            bgcolor="black",
                            border_radius=10,
                            animate=animation.Animation(500, "decelerate"),
                            alignment=alignment.top_left,
                            padding=10,
                            content=MordernNavBar(),
                        ),
                    
                        Container(
                            bgcolor="amber",
                            expand=True,
                            content=Column(
                                expand=True,
                                alignment=MainAxisAlignment.START,
                                # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    mycal,
                                    mycal.output,
                                    TextField(value='Home Page', border=ft.InputBorder.NONE,
                                              text_align=ft.TextAlign.CENTER),
                                    Row(controls=[TextButton(text='Logout', on_click=logout)],
                                        alignment=MainAxisAlignment.CENTER)
                                ],
                            ),
                        ),

                        Column(
                            alignment=alignment.top_right,
                            controls=[
                                Container(
                                    height=400,
                                    width=410,
                                    bgcolor='red',
                                    content=Text('Calendar'),
                                ),

                                Container(
                                    expand=True,
                                    content=Row(
                                        controls=[
                                            Column(
                                                controls=[
                                                    Container(
                                                        expand=True,
                                                        bgcolor='green',
                                                        width=200,
                                                        content=Text('Medical Report'),
                                                    ),
                                                ]
                                            ),
                                            Column(
                                                controls=[
                                                    Container(
                                                        expand=True,
                                                        bgcolor='blue',
                                                        width=200,
                                                        content=Text('Graph'),
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )

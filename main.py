import flet as ft
from flet import *
from flet_route import Routing, path

# Interfaces
from pages.login import Login
from pages.home import Home
from pages.medicalRecord import MedicalRecord
from pages.clinicForm import ClinicForm
from pages.selectHospital import SelectHospital
from pages.selectDoctor import SelectDoctor
from pages.selectDateTime import SelectDateTime
from pages.adminHome import AdminHome
from pages.doctorHome import DoctorHome
from pages.doctorMedicalRecord import DoctorMedicalRecord
from pages.mdSelectHospital import MRSelectHospital

def main(page: Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    app_routes = [
        # Interfaces' path
        path(url='/', clear=True, view=Login().view),  # first page url must be '/'
        path(url='/home', clear=True, view=Home().view),
        path(url='/medicalRecord', clear=False, view=MedicalRecord().view),
        path(url='/mrSelectHospital', clear=False, view=MRSelectHospital().view),
        path(url='/clinicForm', clear=False, view=ClinicForm().view),
        path(url='/selectHospital', clear=False, view=SelectHospital().view),
        path(url='/selectDoctor/:hospital_id', clear=False, view=SelectDoctor().view),
        path(url='/selectDateTime/:hospital_id/:doctor_id', clear=False, view=SelectDateTime().view),
        path(url='/adminHome/:hospital_id', clear=False, view=AdminHome().view),
        path(url='/doctorHome/:doctor_id', clear=False, view=DoctorHome().view),
        path(url='/doctorMedicalRecord/:hospital_id/:doctor_id/:user_id', clear=False, view=DoctorMedicalRecord().view),
    ]
    Routing(page=page, app_routes=app_routes)
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
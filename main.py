import flet as ft
from flet import *
from flet_route import Routing, path

# Interfaces
from pages.login import Login
from pages.register import Register
from pages.clinicForm import ClinicForm
from pages.home import Home
from pages.medicalRecord import MedicalRecord
from pages.doctorList import DoctorList
from pages.selectHospital import SelectHospital
from pages.hospitalInfo import HospitalInfo
from pages.selectDoctor import SelectDoctor
from pages.doctorInfo import DoctorInfo
from pages.selectDateTime import SelectDateTime
from pages.adminHome import AdminHome
from pages.doctorHome import DoctorHome
from pages.patientList import PatientList
from pages.doctorMedicalRecord import DoctorMedicalRecord
from pages.doctorMedicalRecord2 import DoctorMedicalRecord2


def main(page: Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    app_routes = [
        # Interfaces' path
        path(url='/', clear=True, view=Login().view),  # first page url must be '/'
        path(url='/register', clear=True, view=Register().view),
        path(url='/clinicForm', clear=False, view=ClinicForm().view),
        path(url='/home', clear=True, view=Home().view),
        path(url='/medicalRecord', clear=False, view=MedicalRecord().view),
        path(url='/doctorList/:medicalRecord', clear=False, view=DoctorList().view),
        path(url='/selectHospital', clear=False, view=SelectHospital().view),
        path(url='/hospital/info/:hospital_id', clear=False, view=HospitalInfo().view),
        path(url='/selectDoctor/:hospital_id', clear=False, view=SelectDoctor().view),
        path(url='/doctor/info/:doctor_id', clear=False, view=DoctorInfo().view),
        path(url='/selectDateTime/:hospital_id/:doctor_id', clear=False, view=SelectDateTime().view),
        path(url='/adminHome/:hospital_id', clear=False, view=AdminHome().view),
        path(url='/doctorHome/:doctor_id', clear=False, view=DoctorHome().view),
        path(url='/doctor/patientList/:hospital_id/:doctor_id', clear=False, view=PatientList().view),
        path(url='/doctorMedicalRecord/:hospital_id/:doctor_id/:user_id', clear=False, view=DoctorMedicalRecord().view),
        path(url='/doctorMedicalRecord2/:hospital_id/:doctor_id/:user_id', clear=False, view=DoctorMedicalRecord2().view),
    ]
    Routing(page=page, app_routes=app_routes)
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main, assets_dir="assets")
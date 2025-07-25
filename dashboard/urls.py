
from django.urls import path
from . import views

urlpatterns = [
    path('patient/', views.patientDashboard, name='patientDashboard'),
    path('doctor/', views.doctorDashboard, name='doctorDashboard'),
    path('patient/record/', views.records_view, name='records_view'),
    path('patient/appointment/', views.appointment_view, name='appointment_view'),
    path('logout', views.logout, name='logout'),
    path('doctor/record/', views.records_view2, name='records_view2'),
    path('update-appointment-status/<str:aid>/<str:status>/', views.update_appointment_status, name='update_appointment_status'),
    path('patient/forget_passoward/', views.patient_forget_password, name='patient_forget_password'),
    path('doctor/forget_passoward/', views.doctor_forget_password, name='doctor_forget_password'),
]


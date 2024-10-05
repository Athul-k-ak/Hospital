# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_records, name='patient_records'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient/<str:reg_id>/', views.patient_details, name='patient_details'),
    path('register_staff/', views.register_staff, name='register_staff'),
    path('staff_records/', views.staff_records, name='staff_records'),  # New staff records
    path('register_casualty/', views.register_casualty, name='register_casualty'),
    path('casualty_records/', views.casualty_records, name='casualty_records'),  # New casualty records
    path('consultation_records/', views.consultation_records, name='consultation_records'),
    path('delete_consultation/<int:pk>/', views.delete_consultation, name='delete_consultation'),
    path('consult_patient/', views.consult_patient, name='consult_patient'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),
]

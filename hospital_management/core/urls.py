from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Patient Management
    path('patients/', views.patient_records, name='patient_records'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('patient/<str:reg_id>/', views.patient_details, name='patient_details'),
    path('delete_patient/<int:pk>/', views.delete_patient, name='delete_patient'),

    # Staff Management
    path('register_staff/', views.register_staff, name='register_staff'),
    path('staff_records/', views.staff_records, name='staff_records'),

    # Casualty Management
    path('register_casualty/', views.register_casualty, name='register_casualty'),
    path('casualty_records/', views.casualty_records, name='casualty_records'),
    path('delete_casualty/<int:casualty_id>/', views.delete_casualty, name='delete_casualty'),

    # Consultation Management
    path('consultation_records/', views.consultation_records, name='consultation_records'),
    path('consult_patient/', views.consult_patient, name='consult_patient'),
    path('consultation/delete/<int:pk>/', views.delete_consultation, name='delete_consultation'),
]

from django.urls import path

from . import views

app_name = 'HMS1'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('patient_register/', views.PatientRegisterView.as_view(), name='patient_register'),
    path('doctor_register/', views.DoctorRegisterView.as_view(), name='doctor_register'),
    
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    
    path('patient_form/', views.PatientForm.as_view(), name='patient_form'),
    path('patient_profile/', views.PatientProfile.as_view(), name='patient_profile'),
    
    path('appointment/', views.Appointment.as_view(), name='appointment'),
    
    path('pharmacy/', views.Pharmacy.as_view(), name='pharmacy'),
    path('dispense/', views.Dispense.as_view(), name='dispense'),
    path('drug_update/', views.Drug_update.as_view(), name='drug_update'),
    
]
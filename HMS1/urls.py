from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change_form/', auth_views.PasswordChangeView.as_view(), name='password_change_form'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('user_edit/', views.user_edit, name='user_edit'),
    path('patient_record_form/<str:username>/', views.Patientsform, name='patient_record_form'),
    path('appointment/', views.appointment, name='make_appointment'),
    path('inventory/', views.pharmacy, name='inventory'),
    path('search_patients/', views.search_patients, name='search_patients'),
    path('search_drugs/', views.search_drugs, name='search_drugs'),
    path('patient_profile/<str:first_name>/<str:last_name>/', views.patient_profile, name='patient_profile'),
    path('patient_history/', views.patient_history, name='patient_history'),
    path('health_report/<str:username>/', views.health_report_view, name='health_report'),
    path('ticket/<str:first_name>/', views.dispense, name='ticket'),
    path('drug_update/<str:drug_name>/', views.drug_update, name='drug_update'),
]

from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ['is_patient', 'is_doctor','is_frontdesk', 'is_pharmacist', 'first_name', 'last_name', 'username', 'date_of_birth', 'sex', 'phone']
    
@admin.register(PatientVitals)
class PatientVitalAdmin(admin.ModelAdmin):
    list_display = ['patient', 'weight', 'height', 'bp', 'temperature']

@admin.register(MedicalRecord)
class MediacalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date_of_examination', 'symptoms', 'diagnosis', 'prescription']
    
@admin.register(Appointments)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['username', 'date_scheduled', 'time_scheduled', 'seen']
    
@admin.register(Pharmacy_Inventory)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'available']
    
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    nlist_display = [ 'id', 'name', 'user', 'prescriptio']
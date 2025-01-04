from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



# Create your models here.

class user(AbstractUser):
    is_patient = models.BooleanField('patient status', default=False)
    is_doctor = models.BooleanField('doctor status', default=False)
    is_frontdesk = models.BooleanField('frontdesk status', default=False)
    is_pharmacist = models.BooleanField('pharmacist status', default=False)

    # Additional fields
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=10, null=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
class PatientVitals(models.Model):
    patient = models.ForeignKey(user, on_delete=models.CASCADE)
    weight = models.FloatField(max_length=3, null=True)
    height = models.FloatField(max_length=4, null=True)
    bp = models.IntegerField(null=True)
    temperature = models.FloatField(max_length=4, null=True)
    
    @property
    def patient_name(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

class MedicalRecord(models.Model):
    patient = models.ForeignKey(user, on_delete=models.CASCADE)
    date_of_examination = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(null=False, default='')
    diagnosis = models.CharField(max_length=50, null=False, default='')
    prescription = models.TextField(null=False, default='')
    
    @property
    def patient_name(self):
        return f'{self.patient.first_name} {self.patient.last_name}'

    
class Hospital(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)
    address = models.CharField(max_length=50, unique=True, null=False)
    city = models.CharField(max_length=20, null=False)
    

class Appointments(models.Model):
    username = models.CharField(max_length=40, null=False)
    date_scheduled = models.DateField(null=True)
    time_scheduled = models.TimeField(null=True)
    seen = models.BooleanField(default=False)
    
class Pharmacy_Inventory(models.Model):
    name = models.CharField(max_length=20)
    quantity = models.IntegerField()
    available = models.BooleanField(default=False)
    

    
class Ticket(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    patient = models.ForeignKey(user, on_delete=models.CASCADE)
    prescription = models.TextField(null=False)
    dispensed = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.id:  # Only set if it's not already set
            last_ticket = Ticket.objects.all().order_by('id').last()
            if last_ticket:
                self.id = last_ticket.id + 1
            else:
                self.id = 1  # Start from 1 if it's the first ticket
        super().save(*args, **kwargs)
    
    @property
    def patient_name(self):
        return f'{self.patient.first_name} {self.patient.last_name}'
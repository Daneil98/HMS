from django import forms
from .models import *
from socket import fromshare
from django.forms.widgets import DateInput, TimeInput
from django.utils.translation import gettext_lazy as _



#USER ACCOUNT FORMS
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = user
        fields = ('first_name', 'last_name', 'username', 'date_of_birth', 'phone')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match.')
        return cd['password2']



#HOSPITAL FORMS        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ('phone', 'date_of_birth')
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'})
        }
    
class MedicalRecordsForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('symptoms', 'diagnosis', 'prescription')



        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('username', 'date_scheduled', 'time_scheduled')
        widgets = {
            'date_scheduled': DateInput(attrs={'type': 'date'}),
            'time_scheduled': TimeInput(attrs={'type': 'time'})
            
        }
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Pharmacy_Inventory
        fields = '__all__'
        

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('dispensed',)
        
        

class IncreaseButtonForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        label="Increase By",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'})
    )

class DecreaseButtonForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        label="Decrease By",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 70px;'})
    )
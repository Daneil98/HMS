from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import user, MedicalRecord, PatientVitals, Ticket
from .forms import *
from django.contrib import messages
from .decorators import *
from django.http import JsonResponse
from .tasks import *
from .health_summary import get_vital_summary  # We'll create this
import logging

logger = logging.getLogger(__name__)



# Create your views here

def base(request):
    return render(request, 'base.html') 


def index(request):
    return render(request, 'index.html')   


#ACCOUNT VIEWS
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'HMS1/dashboard.html')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'HMS1/login.html', {'form': form})    
    

def patient_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            
            # Check username existence (corrected)
            if user.objects.filter(username=cd['username']).exists():
                user_form.add_error('username', 'This username is already taken')
                return render(request, 'HMS1/patient_register.html', {'user_form': user_form})
            
            try:
                new_user = user.objects.create_user(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    username=cd['username'],
                    password=cd['password'],
                    sex=cd['sex'],
                    date_of_birth=cd['date_of_birth'],
                    phone=cd['phone'],
                    is_patient=True
                )
                return render(request, 'HMS1/register_done.html', {'new_user': new_user})
            except Exception as e:
                user_form.add_error(None, f'Registration error: {str(e)}')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'HMS1/patient_register.html', {'user_form': user_form})


def doctor_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            cd = user_form.cleaned_data
            
            # Check username existence (corrected)
            if user.objects.filter(username=cd['username']).exists():
                user_form.add_error('username', 'This username is already taken')
                return render(request, 'HMS1/doctor_register.html', {'user_form': user_form})
            
            try:
                new_user = user.objects.create_user(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    username=cd['username'],
                    password=cd['password'],
                    sex=cd['sex'],
                    date_of_birth=cd['date_of_birth'],
                    phone=cd['phone'],
                    is_doctor=True
                )
                return render(request, 'HMS1/register_done.html', {'new_user': new_user})
            except Exception as e:
                user_form.add_error(None, f'Registration error: {str(e)}')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'HMS1/doctor_register.html', {'user_form': user_form})




@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'user updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'HMS1/user_edit.html', {'user_form': user_form, 'section': 'edit'})




# HOSPTIAL VIEWS

@login_required
def dashboard(request):
    number = Appointments.objects.filter(seen=False).count()
    finishes = Pharmacy_Inventory.objects.filter(quantity__lte=5).values_list('name', flat=True)
    tickets = Ticket.objects.filter(dispensed=False)   
    
    if number:
        nxt = Appointments.objects.filter(seen=False).order_by('seen').first()        #Get the next/first appointment in a queue 
        next = str(nxt.username)    
    else:
        nxt = Appointments()
        next= None
        
    return render(request, 'HMS1/dashboard.html', {'section': 'dashboard', 'number': number, 'next': next,
                                                   'finishes': list(finishes), 'tickets' : tickets})



@login_required
@doctor_required
def Patientsform(request, username):
    patient = get_object_or_404(user, username=username)
    
    form = MedicalRecordsForm(request.POST)
                                                       
    if request.method == 'POST':
        if form.is_valid():
            
            record = form.save(commit=False)
            # Assign the patient to the record
            record.patient = patient
            # Save the record
            record.save()
            
            Patient = MedicalRecord.objects.filter(patient__username=username).first()
            patient = Patient.patient      #Get the patient that just got attended to
            
            
            Ticket.objects.create(patient=patient, prescription=Patient.prescription)

            appointments = Appointments.objects.filter(username=patient, seen=False)       #Get their appointment record
            appointments.update(seen=True)
            messages.success(request, 'Successfully Updated')
        else:
            form = MedicalRecordsForm()
    return render(request, 'HMS1/patient_record_form.html', {'form': form, 'username': username})
 
 
"""
@login_required
@doctor_required
def Medicalrecords(request):
    records = MedicalRecord.objects.all()
    if records:
        for record in records:
            Name = record.patient
            diagnosis = record.diagnosis
            prescription = record.prescription
            date = record.date_of_examination
    else:
        Name = ''
        diagnosis = ''
        prescription = ''
        date = ''
    
    return render(request, 'HMS1/medical_records.html', { 'Name': Name, 'diagnosis': diagnosis, 'prescription': prescription, 'date': date})

"""

    
@login_required
@doctor_required
def search_patients(request):
    if request.method == 'POST':
        searched = request.POST['Searched']
        patients = user.objects.filter(first_name=searched).order_by('is_patient')
        return render(request, 'HMS1/patient_search.html', {'searched': searched, 'patients': patients, })
    else:
        return render(request, 'HMS1/patient_search.html')
  
     
@login_required
@pharmacist_required
def search_drugs(request):
    if request.method == 'POST':
        searched = request.POST['Searched']
        try:
            drugs = Pharmacy_Inventory.objects.get(name=searched)            
        except Pharmacy_Inventory.DoesNotExist:
            drugs = None 
        return render(request, 'HMS1/drug_search.html', {'searched': searched, 'drugs': drugs})
    else:
        return render(request, 'HMS1/drug_search.html')

           
@login_required
@doctor_required
def patient_profile(request, first_name, last_name):

    records = MedicalRecord.objects.filter(patient__first_name=first_name, patient__last_name = last_name).all()
    vitals = PatientVitals.objects.filter(patient__first_name=first_name, patient__last_name = last_name).first()
    patient = user.objects.filter(first_name = first_name, last_name = last_name).first()
    username = patient.username

    
    return render(request, 'HMS1/patient_profile.html', 
            {'vitals': vitals, 'records': records, 'first_name': first_name, 'last_name': last_name, 'username': username})

 
@login_required
@patient_required
def patient_history(request):
    user_name = request.user.username
    records = MedicalRecord.objects.filter(patient__username=user_name).all()
    vitals = PatientVitals.objects.filter(patient__username=user_name).all()

            
    return render(request, 'HMS1/patient_history.html', 
            {'vitals': vitals, 'records': records, 'username': user_name,})   



@login_required
@patient_required
def health_report_view(request, username):
    username = request.user
    try:
        # Get data from database
        vitals = PatientVitals.objects.filter(patient__username=username)
        
        if not vitals.exists():
            messages.error(request, "This user has no recorded vitals")
            return render(request, 'HMS1/health_report.html', {'username': username})
        
        try:
            # Process with API
            api_response = get_vital_summary(vitals)
            
            # Format response for template
            report_data = {
                'content': api_response['cleaned'],
                'generated_at': api_response['created'],  # Unix timestamp
                'model_used': api_response['model'],
                'username': username
            }
            
            return render(request, 'HMS1/health_report.html', {'report': report_data})
            
        except Exception as api_error:
            logger.error(f"API processing error for {username}: {str(api_error)}")
            messages.error(request, "Failed to generate AI health analysis")
            return render(request, 'HMS1/health_report.html', {'username': username})
            
    except Exception as e:
        logger.error(f"System error generating report for {username}: {str(e)}")
        messages.error(request, "System error generating health report")
        return render(request, 'HMS1/health_report.html', {'username': username})



@login_required
@patient_required
def appointment(request):
    form = AppointmentForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            app = form.save(commit=False)
            date = app.date_scheduled
            time = app.time_scheduled
            conflict = Appointments.objects.filter(Q(date_scheduled=date) & Q(time_scheduled=time) & Q(seen=False)).exists()            #checks if there is a conflict in appointment dates
            if conflict:
                messages.error(request, 'This time slot is already booked. Please pick another.')
            else:
                app.save()   
                messages.success(request, 'Appointment successfully set.')
                form = AppointmentForm(request.POST)
        else:
            messages.error(request, 'There was an error with your submission. Please check your inputs.')

    return render(request, 'HMS1/make_appointment.html', {'form': form})
             
             

@login_required
@pharmacist_required
def pharmacy(request):
    form = InventoryForm(request.POST)
    drugs = Pharmacy_Inventory.objects.all()
    drug_finish.delay()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        else:
            raise ValueError('Form data is not valid')

    return render(request, 'HMS1/inventory.html', {'form': form, 'drugs': drugs})


        
@login_required
@pharmacist_required
def dispense(request, first_name):
    ticket = get_object_or_404(Ticket, patient__username=first_name)
    
    form = TicketForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            ticket.dispensed = True
            ticket.save()
        else:
            raise ValueError('Form data is not valid')

    return render(request, 'HMS1/ticket.html', {'ticket': ticket, 'form': form})
    


@login_required
@pharmacist_required
def drug_update(request, drug_name):
    
    form1 = IncreaseButtonForm(request.POST)
    form2 = DecreaseButtonForm(request.POST)
    drug = get_object_or_404(Pharmacy_Inventory, name=drug_name)
    
    if request.method == 'POST':
        if 'increase' in request.POST:  #Checks if the 'increase' button was clicked
            if form1.is_valid():
                quantity = form1.cleaned_data['quantity']
                increase_inventory(drug_name, quantity)
            else:
                return HttpResponseBadRequest("Invalid data for decreasing quantity.")
        elif 'decrease' in request.POST:  #Checks if the 'decrease' button was clicked
            if form2.is_valid():
                quantity = form2.cleaned_data['quantity']
                #Avoids negative quantities
                decrease_inventory(drug_name, quantity)
            else:
                return HttpResponseBadRequest("Invalid data for decreasing quantity.")
        else:
            return HttpResponseBadRequest("Unknown form submission.")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))          #Redirects back to the same page (refresh)

    # If GET request (optional fallback redirect)
    return redirect('/')
    
 


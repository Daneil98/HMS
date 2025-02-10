from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from ..tasks import *
from .permissions import *

# ACCOUNT API VIEWS

class PatientRegisterView(APIView):
    permission_classes = [AllowAny]
    queryset = user.objects.all()
    
    def post(self, request,):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   #Validates the data
        
        user = serializer.save(is_patient=True)
        
        return Response({'status': 'success', 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)


class DoctorRegisterView(APIView):
    permission_classes = [AllowAny]
    queryset = user.objects.all()
    
    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   #Validates the data
        
        user = serializer.save(is_doctor=True)   
        return Response({'status': 'success', 'message': 'Account created successfully'}, status=status.HTTP_201_CREATED)
    
    
class LoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = user.objects.all()
    serializer_class = LoginSerializer
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'status': 'success', 'message': 'Logged in successfully', "access_token": access_token, "refresh_token": str(refresh)}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'failed', 'message': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
        else:
            raise AuthenticationFailed("Invalid username or password")


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from request data
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                # Blacklist the refresh token
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logout successful"}, status=200)
            return Response({"error": "No refresh token provided"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



class Dashboard(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        number = Appointments.objects.filter(user=request.user, seen=False).count()
        finishes = Pharmacy_Inventory.objects.filter(quantity__lte=5).values_list('name', flat=True)
        tickets = Ticket.objects.filter(dispensed=False) 
        
        content = {
            'number': number,
            'finsihes': finishes,
            'tickets': tickets    
        }

        
        return Response(content, status=status.HTTP_200_OK)



class Patient(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]
 
    def get(self, request, username):           #This function searches for a patient
        serializer = SearchedSerializer(data=request.data)
        
        if serializer.is_valid():
            patient = user.objects.filter(first_name=serializer.first_name).order_by('is_patient')
            return Response({'status': 'success', 'message': 'Patient exists', 'patient': patient}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failed', 'message': 'This patient does not exist'}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def post(self, request, username):
        patient = get_object_or_404(user, username=username)

        serializer = PatientSerializer(data=request.data)
        
        if serializer.is_valid():
            medical_record = serializer.save(patient=patient)
            
            Ticket.objects.create(patient=medical_record, prescription=medical_record.prescription)
    
            appointments = Appointments.objects.filter(username=medical_record.patient, seen=False)       #Get their appointment record
            appointments.update(seen=True)
            return Response({'status': 'success', 'message': 'Patient details saved'}, status=status.HTTP_201_CREATED)
        else:
            return Response(username, serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PatientProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsDoctor]
    
    def get(self, request, first_name, last_name):
        records = MedicalRecord.objects.filter(patient__first_name=first_name, patient__last_name = last_name).all()
        vitals = PatientVitals.objects.filter(patient__first_name=first_name, patient__last_name = last_name).first()
        patient = user.objects.filter(first_name = first_name, last_name = last_name).first()
        
        if not records and not vitals:
            return Response({'status': 'No matching records found'}, status=status.HTTP_404_NOT_FOUND)
        
        content = {
            'user': str(request.user),  
            'records': records,
            'patient': patient,
            'vitals': vitals,
        }
        
        return Response(content, status=status.HTTP_200_OK) 
  
  
class Appointment(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPatient, IsFrontdesk]
    queryset = Appointments.objects.all()
    
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            conflict = Appointments.objects.filter(Q(date_scheduled=serializer.date) & Q(time_scheduled=serializer.time) & Q(seen=False)).exists()            #checks if there is a conflict in appointment dates
            if conflict:
                messages.error(request, 'This time slot is already booked. Please pick another.')
            else:
                serializer.save()
                return Response({'status': 'success', 'message': 'Successfully booked an appointment'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class Pharmacy(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPharmacist]
    
    drug_finish.delay()
    
    def get(self, IsPharmacist):
        drugs = Pharmacy_Inventory.objects.all()
        
        if drugs:
            return Response({'status': 'success'}, drugs, status=status.HTTP_200_OK)
        else:    
            return Response({'status': 'success', 'message': 'There are no drugs in the pharmacy'}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        drugs = Pharmacy_Inventory.objects.all()
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, drugs, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, drugs, status=status.HTTP_400_BAD_REQUEST)
  

class Dispense(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPharmacist]
    
    
    def post(self, request, first_name):
        ticket = get_object_or_404(Ticket, patient__username=first_name)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        
        if serializer.is_valid():
            ticket.dispensed = True
            ticket.save()
            return Response({'satus': 'success'}, ticket, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
        

class Drug_update(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPharmacist]
    
    def post(self, request, drug_name):
        drug = get_object_or_404(Pharmacy_Inventory, name=drug_name)   
        action = request.data.get('action')
        
        if action == 'increase':
            serializer = IncreaseButtonSerialzer(drug, data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data['quantity']
                increase_inventory.delay(drug_name, quantity)    
                return Response({'status': 'success', 'message': f'Inventory increased by {quantity}'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif action == 'decrease':
            serializer = DecreaseButtonSerializer(drug, data=request.data)
            if serializer.is_valid():
                quantity = serializer.validated_data['quantity']
                decrease_inventory.delay(drug_name, quantity)
                return Response({'satus': 'success', 'message': f'Inventory decreased by {quantity}'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Invalid data', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    
    
    
    

from rest_framework import serializers
from django.contrib.auth.models import AbstractUser
from ..models import *


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = AbstractUser
        fields = ['username', 'password',]
        
    def login(self, validated_data):
        password = validated_data.pop('password')
        

class PatientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = user
        fields = ['username', 'first_name', 'last_name', 'password',]
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        # Create the user instance
        user_instance = user.objects.create(**validated_data)

        # Set the hashed password
        user_instance.set_password(password)
        user_instance.is_patient = True  # Mark as a patient
        user_instance.save()

        return user_instance
    

class DoctorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = user
        fields = ['username', 'first_name', 'last_name', 'password',]
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = user(**validated_data)
        user.is_doctor=True
        user.set_password(password)
        user.save()
        return user
    
class PatientFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['symptoms', 'diagnosis', 'prescription']

class SearchedSerializer(serializers.Serializer):
    first_name = serializers.CharField()

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['username', 'date_scheduled', 'time_scheduled']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy_Inventory
        fields = '__all__'
          
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['dispensed']
        
class IncreaseButtonSerialzer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(
        min_value=1, 
        initial=1, 
        label="Increase By",
    )
    
    class Meta:
        model = Pharmacy_Inventory
        fields = ['quantity']

class DecreaseButtonSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(
        min_value=1, 
        initial=1, 
        label="Decrease By",
    )
    
    class Meta:
        model = Pharmacy_Inventory
        fields = ['quantity']

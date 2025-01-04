from rest_framework.permissions import BasePermission

class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_pharmacist

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient
    
class IsFrontdesk(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_frontdesk
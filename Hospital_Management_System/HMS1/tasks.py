from celery import shared_task
from .models import Pharmacy_Inventory

@shared_task
def drug_finish():
    try:
        drugs = Pharmacy_Inventory.objects.all()
        finishes = []
        for drug in drugs:
            if drug.quantity <= 5:
                finishes.append(drug.name)  
    except Pharmacy_Inventory.DoesNotExist:
        return "Drug not found"

@shared_task
def increase_inventory(drug_name, quantity):
    try:
        drug = Pharmacy_Inventory.objects.get(name=drug_name)
        drug.quantity += quantity
        drug.save()
        return f"Inventory updated successfully for drug {drug.name}"
    except Pharmacy_Inventory.DoesNotExist:
        return "Drug not found"
    
    
@shared_task
def decrease_inventory(drug_name, quantity):
    try:
        drug = Pharmacy_Inventory.objects.get(name=drug_name)
        if drug.quantity >= quantity:
            drug.quantity -= quantity
            if drug.quantity == 0:
                drug.available = False
            drug.save()
        return f"Inventory updated successfully for drug {drug.name}"
    except Pharmacy_Inventory.DoesNotExist:
        return "Drug not found"
    

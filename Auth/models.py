
from django.db import models
from django.contrib.auth.models import AbstractUser
from Core.models import Modules

# Create your models here.
class User(AbstractUser):
    avater = models.ImageField(null=True, blank=True)
    
    # permission for machine
    def has_access_to_machine(self):
        setting = Modules.objects.all().first()
        if setting.machine_active == True:
            return True 
        else:
            return False
        
    # permission for spare parts        
    def has_access_to_spareParts(self):
        setting = Modules.objects.all().first()
        if setting.spareParts_active == True:
            return True 
        else:
            return False     
           
    # permission for treasury    
    def has_access_to_treasury(self):
        setting = Modules.objects.all().first()
        if setting.treasurty_active == True:
            return True 
        else:
            return False
    
    # permission for factory                        
    def has_access_to_factory(self):
        setting = Modules.objects.all().first()
        if setting.factory_active == True:
            return True 
        else:
            return False

    # permission for products    
    def has_access_to_products(self):
        setting = Modules.objects.all().first()
        if setting.products_active == True:
            return True 
        else:
            return False        
    
    # permission for wools    
    def has_access_to_wools(self):
        setting = Modules.objects.all().first()
        if setting.wools_active == True:
            return True 
        else:
            return False 
        
               
    # permission for workers    
    def has_access_to_worker(self):
        setting = Modules.objects.all().first()
        if setting.worker_active == True:
            return True 
        else:
            return False        
        
    
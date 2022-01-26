from django.db import models
from Auth.models import User

# Create your models here.
class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الاضافة")
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name = "اضيف بواسطة")
    name = models.CharField(max_length=50 , verbose_name="اسم الشركة")
    phone = models.CharField(max_length=15, verbose_name="موبيل الشركة")
    address = models.CharField(max_length=50, verbose_name="عنوان الشركة")    
    image = models.ImageField(null=True, blank=True, verbose_name="صورة الشركة")
    
    def __str__(self):
        return self.name
    
class WoolType(models.Model):
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الاضافة")
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name = "اضيف بواسطة")
    name = models.CharField(max_length=50 , verbose_name="اسم الخامة")
    
    def __str__(self):
        return self.name
    
            
    

class Wool(models.Model):
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الاضافة")
    created_by = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name = "اضيف بواسطة")
    company = models.ForeignKey(Company, on_delete=models.CASCADE , verbose_name="اسم الشركة")
    wool_type = models.ForeignKey(WoolType, on_delete=models.CASCADE , verbose_name="نوع الخامة")
    quantity = models.IntegerField(verbose_name="الكمية")
    color = models.CharField(max_length=25 , verbose_name="اللون")
    cost = models.IntegerField(verbose_name="سعر الشراء")
    price = models.IntegerField(verbose_name="سعر البيع")
    
  
    def __str__(self):
        return self.name
    
from email.policy import default
from django.db import models
from django.db.models.fields import CharField, DateTimeField

# Create your models here.

class SystemInformation(models.Model):
    logo = models.ImageField(null=True, blank=True, verbose_name="شعارالنظام")
    name = models.CharField(null=True, max_length=50, verbose_name="اسم صاحب النظام")
    phone = models.IntegerField(null=True, verbose_name="رقم الموبيل")
    address = models.CharField(max_length=150, null=True, verbose_name="العنوان")
    
    def __str__(self):
        return self.name
    
    
class Modules(models.Model):
    machine_active  = models.BooleanField(default=True, verbose_name="تنشيط المكينات")
    spareParts_active = models.BooleanField(default=True, verbose_name="تنشيط قطع الغيار")
    treasurty_active = models.BooleanField(default=True, verbose_name="تنشيط الخزينة")
    factory_active = models.BooleanField(default=True, verbose_name="تنشيط المصانع")
    products_active = models.BooleanField(default=True, verbose_name="تنشيط المنتجات")
    wools_active = models.BooleanField(default=True, verbose_name="تنشيط مخازن الصوف ")
    worker_active = models.BooleanField(default=True, verbose_name="تنشيط مخازن العمال ")
    
    def __str__(self):
        return "عناصر النظام"    
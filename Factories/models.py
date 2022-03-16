from datetime import date

from django.db import models
from Auth.models import User

from Products.models import Product

# Create your models here.

class Factory(models.Model):
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الاضافة")
    name = models.CharField(max_length=50 , verbose_name="اسم المصنع")
    hour_price = models.IntegerField(null=True, blank=True, verbose_name="حساب الساعه" )
    machine_type = models.CharField(null=True, blank=True, max_length=50 , verbose_name="نوع المكنة")
    machine_count = models.IntegerField(null=True , verbose_name="عدد المكن")
    phone = models.CharField(null=True, blank=True, max_length=12 , verbose_name="رقم الموبيل")
    active = models.BooleanField(default=True , verbose_name="يعمل")
    start_date = models.DateField(null=True, verbose_name="تاريخ البداية", default=date.today)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاريخ الاضافة")
    price = models.IntegerField(verbose_name="المبلغ")
    factory = models.ForeignKey(Factory , on_delete=models.CASCADE , verbose_name="المصنع")
    recipient = models.CharField(max_length=50 , verbose_name="المستلم")
    admin = models.ForeignKey(User,max_length=50, on_delete=models.CASCADE, null=True, verbose_name="المسئول")
    date = models.DateField(null=True, verbose_name="التاريخ", default=date.today)
    
    def __str__(self):
        return self.factory.name
    
WOOL_TYPE = (
    (1,"قطن"),
    (2,"صوف"),
    (3,"لكرة"),
    (4,"رمش"),
    (5,"سبن"),
    (6,"عصب"),
    (7,"بلستر"),
    (7,"استك"),
)    
         

class FactoryOutSide(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ العملية")
    date = models.DateField(null=True, verbose_name="التاريخ", default=date.today)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, verbose_name="المصنع")
    weight = models.FloatField(null=True, blank=True, verbose_name="الوزن بالكيلو")
    wool_type = models.IntegerField(choices=WOOL_TYPE, null=True, blank=True, verbose_name="نوع الخامة")
    color = models.CharField(null=True, max_length=50, blank=True, verbose_name="اللون")
    percent_loss = models.FloatField(null=True, blank=True, verbose_name="نسبة الهالك")
    weight_after_loss = models.FloatField(null=True, blank=True, verbose_name="الوزن بعد نسبة الهالك")
    admin = models.ForeignKey(User,max_length=50, on_delete=models.CASCADE, null=True, verbose_name="المسئول")
    
    def __str__(self):
        return self.factory.name


PRODUCT_TYPE = (
    (1,"صدر"),
    (2,"ضهر"),
    (3,"كم"),
    (4,"لياقة"),
)    
     
class FactoryInSide(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ العملية")
    date = models.DateField(null=True, verbose_name="التاريخ", default=date.today)
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE, verbose_name="المصنع")
    color = models.CharField(null=True, max_length=50, blank=True, verbose_name="اللون")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,  verbose_name="الموديل")
    
    weight = models.FloatField(null=True, blank=True, verbose_name=" الوزن المستلم بالكيلو")
    product_weight = models.FloatField(null=True, blank=True, verbose_name="وزن القطعة بالجرام")
    product_time = models.FloatField(null=True, blank=True, verbose_name="زمن القطعة دقائق")
    product_count = models.FloatField(null=True, blank=True, verbose_name="عدد القطع")
    product_type = models.IntegerField(choices=PRODUCT_TYPE, null=True, blank=True, verbose_name="نوع القطع")
    wool_type = models.IntegerField(choices=WOOL_TYPE, null=True, blank=True, verbose_name="نوع الخامة")

    
    hour_count = models.FloatField(null=True, blank=True, verbose_name="عدد الساعات")
    hour_price = models.FloatField(null=True, blank=True, verbose_name="سعر الساعة")
    
    total_account = models.FloatField(null=True, blank=True, verbose_name="اجمالي الحساب جنية")
    admin = models.ForeignKey(User,max_length=50, on_delete=models.CASCADE, null=True, verbose_name="المسئول")
    
    def __str__(self):
        return self.factory.name
from random import randint
from django.db import models

from Auth.models import User

# Create your models here.
class Color(models.Model):
    created = models.DateTimeField(auto_now_add =True, verbose_name="تاريخ الاضافة")
    name = models.CharField(max_length=50 , verbose_name="اسم اللون")
    code = models.CharField(max_length=20, verbose_name="كود اللون")
    
    def __str__(self):
        return self.name


CATEGORY= (
    (1, "شبابي"),
    (2, "حريمي"),
    (3, "اولاادي")
    )

SIZE= (
    (1, "S"),
    (2, "M"),
    (3, "L"),
    (3, "XL"),
    (3, "XXL"),
    )

class Product(models.Model):
    created = models.DateTimeField(auto_now=True, verbose_name="تاريخ الاضافة")
    name = models.CharField(max_length=50, verbose_name="اسم الموديل")
    code = models.IntegerField(null=True, blank=True, verbose_name="كود الموديل")
    image = models.ImageField(null=True, blank=True , verbose_name="صورة الموديل")
    weight = models.FloatField(null=True, blank=True ,  verbose_name="وزن الموديل" )
    cost = models.FloatField(null=True, blank=True , max_length=15 , verbose_name="التكلفة")
    price = models.FloatField(null=True, blank=True , verbose_name="سعر البيع")
    color = models.ForeignKey(Color, null=True,  on_delete=models.CASCADE, verbose_name= "اللون")
    size = models.IntegerField(choices=SIZE, default=0, verbose_name= "المقاس")
    category = models.IntegerField(choices=CATEGORY, default=0, verbose_name= "التصنيف")
    quantity = models.IntegerField(null=True, verbose_name="الكمية") 
    deleted = models.BooleanField(default=False)
    
    # To create random code for product
    def save(self, **kwargs):
        if not self.code:
            self.code = randint(10000, 99999)
        return super(Product, self).save(**kwargs)   
    
    def __str__(self):
        return self.name
    
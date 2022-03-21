from datetime import date
from pyexpat import model
from django.db import models

from Auth.models import User

# Create your models here.

WORKER_TYPE = (
    (1, "عامل ارضية"),
    (2, "عامل خياطة"),
    (3, "عامل مكوي"),
    (4, "عامل مكينة"),
    (5, "عامل عادي")
)

class Worker(models.Model):
    name = models.CharField(max_length=30, verbose_name="اسم العامل")
    image = models.ImageField(verbose_name="صورة العامل", null=True, blank=True)
    phone = models.IntegerField(null=True, verbose_name="رقم الموبيل")
    worker_type = models.IntegerField(choices=WORKER_TYPE, verbose_name="نوع العامل")
    day_cost = models.FloatField(default=0, null=True, verbose_name="تكلفة اليوم")
    deleted = models.BooleanField(default=False, verbose_name="حذف")
    
    def __str__(self):
        return self.name
    
    
HOUR_COUNT = (
    (1, "6"),
    (2, "8"),
    (3, "12"),
    (4, "18"),
)

class WorkerAttendance(models.Model):
    date = models.DateField(verbose_name="تاريخ الحضور")    
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE,verbose_name="العامل")    
    hour_count = models.IntegerField(choices=HOUR_COUNT,  verbose_name="عدد الساعات")
    attend = models.BooleanField(default=0, verbose_name="حضر")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المسئول")
    
    def __str__(self):
        return self.worker.name
    
class WorkerPayment(models.Model):
    date = models.DateField(verbose_name="تاريخ السحب") 
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, verbose_name=" العامل") 
    price = models.FloatField(verbose_name="المبلغ") 
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المسئول")
    
    def __str__(self):
        return self.worker.name
    
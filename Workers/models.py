from pyexpat import model
from django.db import models

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
    phone = models.IntegerField(null=True, verbose_name="رقم الموبيل")
    worker_type = models.IntegerField(choices=WORKER_TYPE, verbose_name="نوع العامل")
    day_cost = models.FloatField(default=0, null=True, verbose_name="تكلفة اليوم")
    deleted = models.BooleanField(default=False, verbose_name="حذف")
    
    def __str__(self):
        return self.name
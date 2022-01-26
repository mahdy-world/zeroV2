from django.db import models
from django.utils.timezone import now

# Create your models here.

class WorkTreasury(models.Model):
    name = models.CharField(max_length=20, verbose_name="اسم الخزينة")
    balance = models.FloatField(default=0, verbose_name='الرصيد')
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class HomeTreasury(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    balance = models.FloatField(default=0.0, verbose_name='الرصيد')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    account_no = models.CharField(max_length=128, verbose_name='رقم الحساب', null=True, blank=True)
    balance = models.FloatField(default=0.0, verbose_name='الرصيد')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


TRANSACTION_CHOICES = (
    (1, "مشتريات"),
    (2, "مبيعات"),
    (3, "سحب يدوي"),
    (4, "ايداع يدوي"),
    )

TRANSACTION_CHOICES2 = (
    (1, "مشتريات"),
    (2, "مبيعات"),
    (3, "سحب يدوي"),
    (4, "ايداع يدوي"),
)

class WorkTreasuryTransactions(models.Model):
    transaction = models.CharField(max_length=255, null=True, blank=True, verbose_name='عملية')
    treasury = models.ForeignKey(WorkTreasury, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الخزنة')
    transaction_type = models.IntegerField(choices=TRANSACTION_CHOICES, default=0, verbose_name="نوع العملية")
    value = models.FloatField(default=0.0, verbose_name='القيمة')
    date = models.DateTimeField(default=now, verbose_name='التاريخ')

    def __str__(self):
        return self.treasury.name


class HomeTreasuryTransactions(models.Model):
    transaction = models.CharField(max_length=255, null=True, blank=True, verbose_name='عملية')
    treasury = models.ForeignKey(HomeTreasury, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الخزنة')
    transaction_type = models.IntegerField(choices=TRANSACTION_CHOICES, default=0, verbose_name="نوع العملية")
    value = models.FloatField(default=0.0, verbose_name='القيمة')
    date = models.DateTimeField(default=now, verbose_name='التاريخ')

    def __str__(self):
        return self.treasury.name


class BankAccountTransactions(models.Model):
    transaction = models.CharField(max_length=255, null=True, blank=True, verbose_name='عملية')
    account = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='الحساب')
    transaction_type = models.IntegerField(choices=TRANSACTION_CHOICES2, default=0, verbose_name="نوع العملية")
    value = models.FloatField(default=0.0, verbose_name='القيمة')
    date = models.DateTimeField(default=now, verbose_name='التاريخ')

    def __str__(self):
        return self.account.name
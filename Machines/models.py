from django.db import models
from django.db.models.deletion import CASCADE
from SpareParts.models import SparePartsNames, SparePartsOrders
from Treasury.models import *


# Create your models here.
# انواع الماكينات
class MachinesTypes(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name


# مخازن الماكينات
class MachinesWarehouses(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم المخزن')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# اسماء الماكينات
class MachinesNames(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم الصنف')
    machine_type = models.ForeignKey(MachinesTypes, on_delete=models.CASCADE,null="True", verbose_name="نوع المكينة")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    


# # موردين الماكينات
# STATUS_CHOICES = (
#     (2, "عليك للمورد"),
#     (1, "لك عند المورد"),
#     )


class MachinesSuppliers(models.Model):
    name = models.CharField(max_length=250, verbose_name='اسم المورد')
    phone = models.CharField(max_length=11, verbose_name='رقم الهاتف')
    # initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    # credit_or_debit = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='لك أم عليك')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


# فاتورة طلب الماكينات
class MachinesOrders(models.Model):
    order_number = models.CharField(max_length=50, null=True, verbose_name="رقم الطلب")
    order_date = models.DateField(null=True, verbose_name="تاريخ الطلب")
    order_supplier = models.ForeignKey(MachinesSuppliers, on_delete=models.CASCADE, null=True, verbose_name='المورد')
    order_deposit_value = models.FloatField(default=0, null=True, verbose_name="قيمة العربون")
    order_deposit_date = models.DateField(null=True, verbose_name="تاريخ دفع العربون")
    order_rest_date = models.DateField(null=True, verbose_name="تاريخ دفع باقي المبلغ")
    order_receipt_date = models.DateField(null=True, verbose_name="تاريخ استلام البضاعة")
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.order_number


# منتجات داخل فاتورة طلب الماكينات
class MachinesOrderProducts(models.Model):
    product_order = models.ForeignKey(MachinesOrders, on_delete=models.CASCADE, null=True, verbose_name='الطلبية')
    product_name = models.ForeignKey(MachinesNames, on_delete=models.CASCADE, null=True, verbose_name='المنتج')
    product_quantity = models.IntegerField(default=0, null=True, verbose_name="الكمية")
    product_price = models.FloatField(default=0, null=True, verbose_name="سعر الشراء")
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.product_order


OPERATIONS_CHOICES = (
    (1, "دفع عربون"),
    (2, "دفع باقي المبلغ"),
    (3, "دفع مبلغ تخليص البضاعة"),
    (4, "استلام البضاعة"),
    (5, "دفع الضرائب"),
    )


class MachinesOrderOperations(models.Model):
    order_number = models.ForeignKey(MachinesOrders, on_delete=models.CASCADE, verbose_name="رقم الطلب")
    operation_date = models.DateTimeField(null=True, verbose_name="تاريخ العملية")
    operation_type = models.IntegerField(choices=OPERATIONS_CHOICES, default=0, verbose_name="نوع العملية")
    operation_value = models.FloatField(default=0, verbose_name="قيمة العملية")
    treasury_name = models.ForeignKey(WorkTreasury, on_delete=models.CASCADE, null=True, verbose_name='الخزنة المستخدمة')
    warehouse_name = models.ForeignKey(MachinesWarehouses, on_delete=models.CASCADE, null=True, verbose_name='المخزن المستخدم')


class WarehouseTransactions(models.Model):
    warehouse = models.ForeignKey(MachinesWarehouses, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='المخزن')
    item = models.ForeignKey(MachinesNames, on_delete=models.SET_NULL, null=True, verbose_name='المنتج')
    quantity = models.FloatField(default=0.0, verbose_name='الكمية')
    purchase_cost = models.FloatField(default=0.0, verbose_name='سعر الشراء')

    def __str__(self):
        return self.warehouse.name
    



NOTIFECATION_CHOICES = (
        (1, "موعد دفع عربون مكينة"),
        (2, "موعد دفع باقي مبلغ مكينة"),
        (3, "موعد استلام بضاعة مكينة"),
        (4, "موعد دفع ضرائب مكينة"),
        (5, "موعد دفع عربون قطع غيار"),
        (6, "موعد دفع باقي مبلغ قطع غيار"),
        (7, "موعد استلام بضاعة قطع غيار"),
        (8, "موعد ضرائب قطع غيار"),
    )   
class MachineNotifecation(models.Model):
    created_at = models.DateField(null=True,  verbose_name="تاريخ الانشاء")
    machine_order = models.ForeignKey(MachinesOrders, null=True, on_delete=models.CASCADE, verbose_name="طلبية المكن")
    spare_order = models.ForeignKey(SparePartsOrders, null=True, on_delete=models.CASCADE, verbose_name="طلبية قطع الغيار")
    notifeaction_type = models.IntegerField(choices=NOTIFECATION_CHOICES, default=0, verbose_name="نوع الاشعار")
    message = models.CharField(max_length=100, null=True, verbose_name=" الرسالة")
    read = models.BooleanField(default=0, verbose_name="قرأت / لم تقرأ")
    
    def __str__(self):
        return self.message
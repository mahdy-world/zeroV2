from django.db import models

from Treasury.models import WorkTreasury


# Create your models here.

# انواع قطع الغيار
class SparePartsTypes(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    deleted = models.BooleanField(default=False, verbose_name='مسح')

    def __str__(self):
        return self.name


# مخازن قطع الغيار
class SparePartsWarehouses(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم المخزن')
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# اسماء قطع الغيار
class SparePartsNames(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم الصنف')
    spare_type = models.ForeignKey(SparePartsTypes, on_delete=models.CASCADE, verbose_name="نوع قطعة الغيار")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# موردين قطع الغيار
# STATUS_CHOICES = (
#     (2, "عليك للمورد"),
#     (1, "لك عند المورد"),
#     )

class SparePartsSuppliers(models.Model):
    name = models.CharField(max_length=250, verbose_name='اسم المورد')
    phone = models.CharField(max_length=11, verbose_name='رقم الهاتف')
    # initial_balance = models.FloatField(default=0, verbose_name='الرصيد الافتتاحي')
    # credit_or_debit = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='لك أم عليك')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


#  الطلب
class SparePartsOrders(models.Model):
    order_number = models.CharField(max_length=50, null=True, verbose_name="رقم الطلب")
    order_date = models.DateField(null=True, verbose_name="تاريخ الطلب")
    order_supplier = models.ForeignKey(SparePartsSuppliers, on_delete=models.CASCADE, null=True, verbose_name='المورد')
    order_deposit_value = models.FloatField(default=0, null=True, verbose_name="قيمة العربون")
    order_deposit_date = models.DateField(null=True, verbose_name="تاريخ دفع العربون")
    order_rest_date = models.DateField(null=True, verbose_name="تاريخ دفع باقي المبلغ")
    order_receipt_date = models.DateField(null=True, verbose_name="تاريخ استلام البضاعة")
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.order_number


# منتجات  الفاتورة
class SparePartsOrderProducts(models.Model):
    product_order = models.ForeignKey(SparePartsOrders, on_delete=models.CASCADE, null=True, verbose_name='الطلبية')
    product_name = models.ForeignKey(SparePartsNames, on_delete=models.CASCADE, null=True, verbose_name='المنتج')
    product_quantity = models.IntegerField(default=0, null=True, verbose_name="الكمية")
    product_price = models.FloatField(default=0, null=True, verbose_name="سعر الشراء")
    deleted = models.BooleanField(default=False, verbose_name='حذف')


OPERATIONS_CHOICES = (
    (1, "دفع عربون"),  
    (2, "دفع باقي المبلغ"),
    (3, 'دفع مبلغ تخليص البضاعة'),
    (4, "استلام البضاعة"),
    (5, "دفع الضرائب"),
    )

class SparePartsOrderOperations(models.Model):
    order_number = models.ForeignKey(SparePartsOrders, on_delete=models.CASCADE, verbose_name="رقم الطلب")
    operation_date = models.DateTimeField(null=True, verbose_name="تاريخ العملية")
    operation_type = models.IntegerField(choices=OPERATIONS_CHOICES, default=0, verbose_name="نوع العملية")
    operation_value = models.FloatField(default=0, verbose_name="قيمة العملية")
    treasury_name = models.ForeignKey(WorkTreasury, null=True, on_delete=models.CASCADE, verbose_name="الخزنة المستخدمة")
    warehouse_name = models.ForeignKey(SparePartsWarehouses,null=True, on_delete=models.CASCADE, verbose_name="المخزن المستخدم")


class SparePartsWarehouseTransactions(models.Model):
    warehouse = models.ForeignKey(SparePartsWarehouses,null=True, verbose_name="المخزن", on_delete=models.CASCADE)
    item = models.ForeignKey(SparePartsNames,null=True, verbose_name="المنتجات", on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0, verbose_name="الكمية")    
    price_cost = models.FloatField(default=0.0, verbose_name="سعر الشراء")    
    
  


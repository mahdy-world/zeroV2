from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(SparePartsTypes)
admin.site.register(SparePartsSuppliers)
admin.site.register(SparePartsOrders)
admin.site.register(SparePartsOrderProducts)
admin.site.register(SparePartsOrderOperations)
admin.site.register(SparePartsWarehouses)
admin.site.register(SparePartsWarehouseTransactions)
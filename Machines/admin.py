from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MachinesTypes)
admin.site.register(MachinesWarehouses)
admin.site.register(MachinesNames)
admin.site.register(MachinesSuppliers)
admin.site.register(MachinesOrders)
admin.site.register(MachinesOrderProducts)
admin.site.register(MachinesOrderOperations)
admin.site.register(WarehouseTransactions)
admin.site.register(MachineNotifecation)

import datetime
from itertools import product
from django.http import request
from Core.models import SystemInformation
from Factories.models import Factory
from Products.models import Product, ProductSellers
from SpareParts.models import *
from Machines.models import * 
from django.utils import timezone as tz
from django.db.models import Q

from Workers.models import Worker



def allcontext(request):
    info = SystemInformation.objects.filter(id=1)
    spare_parts = SparePartsNames.objects.filter(deleted=0)
    machines = MachinesNames.objects.filter(deleted=False)
    factorys = Factory.objects.filter(deleted=False)
    spare_order = SparePartsOrders.objects.filter(deleted=False)
    machine_order = MachinesOrders.objects.filter(deleted=False)
    products = Product.objects.filter(deleted=False)
    sellers = ProductSellers.objects.filter(deleted=False)
    workers = Worker.objects.filter(deleted=False)
    
    
    
    machine_order_count = machine_order.count() # عدد طلبيات المكينات
    spare_order_count = spare_order.count() # عدد طلبيات قطع الغيار
    spare_supplier_count = SparePartsSuppliers.objects.filter(deleted=False).count() # عدد موردين قطع الغيار
    machines_count = machines.count()
    spareparts_count = spare_parts.count()
    machines_supplier  = MachinesSuppliers.objects.filter(deleted=False).count()
    
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    
    notfaiy = MachineNotifecation.objects.filter(Q(created_at=tomorrow) | Q(created_at = today ) ).order_by('-created_at')
    notification_count = MachineNotifecation.objects.filter(Q(created_at=tomorrow) | Q(created_at = today ), read=False ).count()

    context = { 
        'info':info,
        'spare_parts':spare_parts,
        'machines':machines,
        'spare_order':spare_order,
        'machine_order':machine_order,
        'notifay':notfaiy,
        'today': today,
        'tomorrow' : tomorrow,
        'notification_count': notification_count,
        'machine_order_count' : machine_order_count,
        'spare_order_count' : spare_order_count,
        'spare_supplier_count' : spare_supplier_count,
        'machines_count' : machines_count,
        'spareparts_count' : spareparts_count,
        'machines_supplier' : machines_supplier,
        'factorys' : factorys,
        'products':products,
        'sellers':sellers,
        'workers':workers,
        

    }
    return context
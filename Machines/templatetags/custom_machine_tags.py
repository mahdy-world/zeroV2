from django import template
from django.db.models import Sum

register = template.Library()
from Machines.models import *

@register.simple_tag(name='order_products')
def order_products(order_id):
    return MachinesOrderProducts.objects.filter(product_order__id=order_id)


@register.simple_tag(name='order_op1')
def order_op1(order_id):
    return MachinesOrderOperations.objects.filter(order_number__id=order_id, operation_type=1)


@register.simple_tag(name='order_op2')
def order_op2(order_id):
    return MachinesOrderOperations.objects.filter(order_number__id=order_id, operation_type=2)


@register.simple_tag(name='order_op3')
def order_op3(order_id):
    return MachinesOrderOperations.objects.filter(order_number__id=order_id, operation_type=3)


@register.simple_tag(name='order_op4')
def order_op4(order_id):
    return MachinesOrderOperations.objects.filter(order_number__id=order_id, operation_type=4)


@register.simple_tag(name='order_op5')
def order_op5(order_id):
    return MachinesOrderOperations.objects.filter(order_number__id=order_id, operation_type=5)


@register.simple_tag(name='order_products_val')
def order_products_val(order_id):
    return MachinesOrderProducts.objects.filter(product_order__id=order_id).aggregate(sum=Sum('product_price')).get('sum')


@register.simple_tag(name='warehouse_products')
def warehouse_products(ware_id):
    return WarehouseTransactions.objects.filter(warehouse__id=ware_id)
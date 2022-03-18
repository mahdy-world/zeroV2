from django import template
from django.db.models import Sum

register = template.Library()
from Products.models import *


@register.simple_tag(name='sellers_debit')
def sellers_debit(seller_id):
    seller_initial_debit = ProductSellers.objects.get(id=seller_id).initial_balance_debit
    seller_payments = SellerPayments.objects.filter(seller__id=seller_id).aggregate(sum=Sum('paid_value')).get('sum')
    if seller_initial_debit:
        seller_initial_debit = seller_initial_debit
    else:
        seller_initial_debit = 0

    if seller_payments:
        seller_payments = seller_payments
    else:
        seller_payments = 0
    return float(seller_initial_debit) - float(seller_payments)
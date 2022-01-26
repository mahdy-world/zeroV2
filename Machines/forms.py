from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import *


class MachinesTypesForm(forms.ModelForm):
    class Meta:
        model = MachinesTypes
        exclude = ['deleted']


class MachinesTypesFormDelete(forms.ModelForm):
    class Meta:
        model = MachinesTypes
        exclude = ['name']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


#######################################################


class MachinesWarehousesForm(forms.ModelForm):
    class Meta:
        model = MachinesWarehouses
        exclude = ['deleted']


class MachinesWarehousesFormDelete(forms.ModelForm):
    class Meta:
        model = MachinesWarehouses
        exclude = ['name']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


#######################################################


class MachinesNamesForm(forms.ModelForm):
    class Meta:
        model = MachinesNames
        exclude = ['deleted']


class MachinesNamesFormDelete(forms.ModelForm):
    class Meta:
        model = MachinesNames
        exclude = ['name', 'machine_type']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


#######################################################


class MachinesSuppliersForm(forms.ModelForm):
    class Meta:
        model = MachinesSuppliers
        exclude = ['deleted']


class MachinesSuppliersFormDelete(forms.ModelForm):
    class Meta:
        model = MachinesSuppliers
        exclude = ['name', 'phone', 'initial_balance', 'credit_or_debit']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


#######################################################


class MachinesOrdersForm(forms.ModelForm):
    class Meta:
        model = MachinesOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier': forms.Select(attrs={'class': 'form-control' , 'name':'order_supplier'}),
            'order_deposit_value': forms.NumberInput(attrs={'class': 'form-control' , 'name':'order_deposit_value'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'name':'order_number'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'name':'order_date' }),
            'order_deposit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control' , 'name':'deposit_date'}),
            'order_rest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'name':'order_rest_date'}),
            'order_receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'name':'order_receipt_date'}),
        }


class MachinesOrdersFormOp1(forms.ModelForm):
    class Meta:
        model = MachinesOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_deposit_value': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'order_deposit_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'order_rest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'order_receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MachinesOrdersFormOp1, self).__init__(*args, **kwargs)
        self.fields['order_supplier'].empty_label = None


class MachinesOrdersFormOp2(forms.ModelForm):
    class Meta:
        model = MachinesOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_deposit_value': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'order_deposit_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'order_rest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'readonly': 'readonly'}),
            'order_receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MachinesOrdersFormOp2, self).__init__(*args, **kwargs)
        self.fields['order_supplier'].empty_label = None


class MachinesOrdersDeleteForm(forms.ModelForm):
    class Meta:
        exclude = ['order_number', 'order_date', 'order_supplier', 'order_deposit_value', 'order_deposit_date',
                   'order_rest_date', 'order_receipt_date']
        model = MachinesOrders
        widgets = {

            'deleted': forms.HiddenInput(),
        }


class MachinesOrderProductsForm(forms.ModelForm):
    class Meta:
        model = MachinesOrderProducts
        fields = ['product_name', 'product_quantity', 'product_price']
        widgets = {

            'product_name': forms.Select(attrs={'class': 'form-control', 'id': 'product'}),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'product_price': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),

        }


class MachinesOrderProductsDeleteForm(forms.ModelForm):
    class Meta:
        model = MachinesOrderProducts
        exclude = ['product_name', 'product_quantity', 'product_price', 'product_order']
        widgets = {

            'deleted': forms.HiddenInput(),
        }


class MachinesOrderOperationsForm(forms.ModelForm):
    class Meta:
        model = MachinesOrderOperations
        fields = ['operation_value', 'treasury_name', 'operation_date']
        widgets = {
            'operation_value': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class MachinesOrderOperationsForm2(forms.ModelForm):
    class Meta:
        model = MachinesOrderOperations
        fields = ['warehouse_name', 'operation_date']
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class MachinesOrderOperationsForm3(forms.ModelForm):
    class Meta:
        model = MachinesOrderOperations
        fields = ['operation_value', 'treasury_name', 'operation_date']
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
        

from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import widgets
from django.forms.models import inlineformset_factory
from .models import *

class SparePartsTypeForm(forms.ModelForm):
    class Meta:
        model = SparePartsTypes
        exclude = ['deleted']

class DeleteTypeForm(forms.ModelForm):
    class Meta:
        exclude = ['name']
        model = SparePartsTypes
        widgets = {

            'deleted': forms.HiddenInput(),
        }
        
class SparePartsNameForm(forms.ModelForm):
    class Meta:
        model = SparePartsNames
        exclude = ['deleted']        
        
        

class DeleteNameForm(forms.ModelForm):
    class Meta:
        exclude = ['name']
        model = SparePartsNames
        widgets = {

            'deleted': forms.HiddenInput(),
        }
                
                
                

class SparePartsWarehouseForm(forms.ModelForm):
    class Meta:
        model = SparePartsWarehouses
        exclude = ['deleted']        
        
        

class WarehouseDeleteForm(forms.ModelForm):
    class Meta:
        exclude = ['name']
        model = SparePartsWarehouses
        widgets = {

            'deleted': forms.HiddenInput(),
        }

class SparePartSupplierForm(forms.ModelForm):
    class Meta:
        model = SparePartsSuppliers
        exclude = ['deleted']        
        
        

class SupplierDeleteForm(forms.ModelForm):
    class Meta:
        exclude = ['name', 'phone', 'initial_balance', 'credit_or_debit']
        model = SparePartsSuppliers
        widgets = {

            'deleted': forms.HiddenInput(),
        }


class SparePartOrderForm(forms.ModelForm):
    class Meta:
        model = SparePartsOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier':forms.Select(attrs={'class':'form-control'}),
            'order_deposit_value':forms.NumberInput(attrs={'class':'form-control'}),
            'order_number':forms.TextInput(attrs={'class':'form-control'}),
            'order_date' :forms.DateInput(attrs={'type': 'date','class':'form-control' }),
            'order_deposit_date' :forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'order_rest_date' :forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'order_receipt_date' :forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        }

class SparePartOrderFormOp1(forms.ModelForm):
    class Meta:
        model = SparePartsOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier':forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_deposit_value':forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_number':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_date':forms.DateInput(attrs={'type': 'date','class':'form-control', 'readonly':'readonly'}),
            'order_deposit_date' :forms.DateInput(attrs={'type': 'date','class':'form-control', 'readonly':'readonly'}),
            'order_rest_date' :forms.DateInput(attrs={'type': 'date','class':'form-control'}),
            'order_receipt_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SparePartOrderFormOp1, self).__init__(*args, **kwargs)
        self.fields['order_supplier'].empty_label = None

class SparePartOrderFormOp2(forms.ModelForm):
    class Meta:
        model = SparePartsOrders
        exclude = ['deleted']
        widgets = {
            'order_supplier':forms.Select(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_deposit_value':forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_number':forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}),
            'order_date':forms.DateInput(attrs={'type': 'date','class':'form-control', 'readonly':'readonly'}),
            'order_deposit_date' :forms.DateInput(attrs={'type': 'date','class':'form-control', 'readonly':'readonly'}),
            'order_rest_date' :forms.DateInput(attrs={'type': 'date','class':'form-control', 'readonly':'readonly'}),
            'order_receipt_date':forms.DateInput(attrs={'type': 'date','class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SparePartOrderFormOp2, self).__init__(*args, **kwargs)
        self.fields['order_supplier'].empty_label = None


class OrderDeleteForm(forms.ModelForm):
    class Meta:
        exclude = ['order_number', 'order_date', 'order_supplier', 'order_deposit_value', 'order_deposit_date', 'order_rest_date', 'order_receipt_date']
        model = SparePartsOrders
        widgets = {

            'deleted': forms.HiddenInput(),
        }


class orderProductForm(forms.ModelForm):
    class Meta:
        model = SparePartsOrderProducts
        fields = ['product_name','product_quantity', 'product_price']
        widgets = {

            'product_name':forms.Select(attrs={'class':'form-control' , 'id':'product' }),
            'product_quantity':forms.NumberInput(attrs={'class':'form-control', 'min':'1'}),
            'product_price':forms.NumberInput(attrs={'class':'form-control', 'min':'1'}),
            
        }        

class orderProductDeleteForm(forms.ModelForm):
    class Meta:
        model = SparePartsOrderProducts
        exclude = ['product_name','product_quantity', 'product_price', 'product_order']
        widgets = {

            'deleted': forms.HiddenInput(),
        }
    

# دفع العربون
class OperationForm(forms.ModelForm):
    class Meta:
        model = SparePartsOrderOperations
        fields = ['operation_value', 'treasury_name', 'operation_date']
        widgets = {
            'operation_value': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

# استلام البضاعة
class OperationsForm2(forms.ModelForm):
    class Meta:
        model = SparePartsOrderOperations
        fields = ['warehouse_name', 'operation_date']
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }



# تخليص البضاعة
class OperationsForm3(forms.ModelForm):
    class Meta:
        model = SparePartsOrderOperations                                                                             

        fields = ['operation_value', 'treasury_name', 'operation_date']
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),}


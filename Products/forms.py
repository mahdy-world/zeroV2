from dataclasses import fields
from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['deleted', 'code']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'weight': forms.NumberInput(attrs={'class':'form-control'}),
            'cost': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'color': forms.Select(attrs={'class':'form-control'}),
            'size': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control'}),
        }


class ProductFormUpdate(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['deleted', 'code']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'}),
            'weight': forms.NumberInput(attrs={'class':'form-control'}),
            'cost': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'color': forms.Select(attrs={'class':'form-control'}),
            'size': forms.Select(attrs={'class':'form-control'}),
            'category': forms.Select(attrs={'class':'form-control'}),
            'quantity': forms.NumberInput(attrs={'class':'form-control', 'readonly':'readonly'}),
        }


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Product
        widgets = {
            'deleted' : forms.HiddenInput()
        }


class ProductQuantityForm(forms.ModelForm):
    add_quant = forms.IntegerField(label='اضافة كمية جديدة')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['add_quant'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ادخل كمية هنا ..'})
        self.fields['quantity'].label = 'الكمية الموجودة'

    class Meta:
        model = Product
        fields = ['quantity', 'add_quant']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class ProductSellerForm(forms.ModelForm):
    class Meta:
        model = ProductSellers
        exclude = ['deleted']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'initial_balance_debit': forms.NumberInput(attrs={'class':'form-control'}),
        }


class ProductSellerFormUpdate(forms.ModelForm):
    class Meta:
        model = ProductSellers
        exclude = ['deleted', 'initial_balance_debit']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
        }


class ProductSellerDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Product
        widgets = {
            'deleted' : forms.HiddenInput()
        }


class ProductSellerPaymentForm(forms.ModelForm):
    class Meta:
        model = SellerPayments
        fields = ['paid_value']
        widgets = {
            'paid_value': forms.NumberInput(attrs={'class': 'form-control'}),
        }
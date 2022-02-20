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
        
class ProductDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Product
        widgets = {
            'deleted' : forms.HiddenInput()
        }              
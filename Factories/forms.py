from pyexpat import model
from django import forms
from .models import *
from django.utils.timezone import now

class FactoryForm(forms.ModelForm):
    class Meta:
        model = Factory
        exclude = ['deleted']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'hour_price' : forms.NumberInput(attrs={'class':'form-control'}),
            'machine_type' : forms.TextInput(attrs={'class':'form-control'}),
            'machine_count' : forms.NumberInput(attrs={'class':'form-control'}),
            'phone' : forms.TextInput(attrs={'class':'form-control'}),
            'start_date' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'active' : forms.CheckboxInput(attrs={'class':'form-control'}),
            
        }
        
class FactoryDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Factory
        widgets = {
            'deleted' : forms.HiddenInput()
        }        
        
        
class FactoryPaymentForm(forms.ModelForm):
    class Meta:
        fields = ['date', 'price', 'admin', 'recipient']
        model = Payment
        widgets = {
            'date' : forms.TextInput(attrs={'type':'date', 'class':'form-control',  'placeholder':'تاريخ السحب...', 'id':'date'}),
            'price' : forms.NumberInput(attrs={ 'class':'form-control', 'placeholder':'المبلغ...', 'id':'price'}),
            'admin' : forms.Select(attrs={'class':'form-control',  'placeholder':'المسئول...', 'id':'admin'}),
            'recipient' : forms.TextInput(attrs={'class':'form-control',  'placeholder':'المستلم...', 'id':'recipient'}),
        }
        
class FactoryPaymentReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date',
        'name':'form_date',
        'class':'form-control',
        'placeholder':'من ...'}),
        label= 'من',
        initial=now().date().isoformat())
         
    to_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date',
        'name':'to_date',
        'class':'form-control',
        'placeholder':'الي ...'}),
        label= 'الي',
        initial=now().date().isoformat())     
        
        
class FactoryOutSideForm(forms.ModelForm):
    class Meta:
        fields = ['date', 'weight', 'color', 'percent_loss', 'weight_after_loss', 'admin' ]
        model = FactoryOutSide
        widgets = {
            'date' : forms.TextInput(attrs={'type':'date', 'class':'form-control',  'placeholder':'تاريخ الخروج...', 'id':'date'}),
            'admin' : forms.TextInput(attrs={'class':'form-control', 'min':'1', 'placeholder':'المسئول...', 'id':'admin'}),
            'weight' : forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'placeholder':'الوزن...', 'id':'weight'}),
            'color' : forms.TextInput(attrs={'class':'form-control', 'min':'1', 'placeholder':'اللون...', 'id':'color'}),
            'percent_loss' : forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'placeholder':'نسبة الهالك...', 'id':'percent_loss'}),
            'weight_after_loss' : forms.NumberInput(attrs={'class':'form-control', 'min':'1', 'placeholder':'الوزن بعدالهالك...', 'id':'weight_after_loss'}),
        }
        
        
class FactoryInSideForm(forms.ModelForm):
    class Meta:
        fields = ['date', 'weight', 'color', 'product', 'product_weight', 
                  'product_time', 'product_count','hour_count', 'hour_price',
                  'total_account', 'admin']
        model = FactoryInSide
        widgets = {
            'date' : forms.TextInput(attrs={'type':'date', 'class':'form-control',  'placeholder':'تاريخ الاستلام...', 'id':'date'}),
            'weight' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':'الوزن المستلم...', 'id':'weight'}),
            'color' : forms.TextInput(attrs={ 'class':'form-control', 'placeholder':' اللون...', 'id':'color'}),
            'product' : forms.TextInput(attrs={ 'class':'form-control', 'placeholder':' المنتج...', 'id':'product'}),
            'product_weight' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':' وزن القطعة...', 'id':'product_weight'}),
            'product_time' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':' وقت القطعة...', 'id':'product_time'}),
            'product_count' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':'  عدد القطع...', 'id':'product_count'}),
            'hour_count' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':'  عدد الساعات...', 'id':'hour_count'}),
            'hour_price' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':'سعر الساعة...', 'id':'hour_price'}),
            'total_account' : forms.NumberInput(attrs={ 'class':'form-control', 'min':'1', 'placeholder':'اجمالي الحساب...', 'id':'total_account'}),
            'admin' : forms.TextInput(attrs={ 'class':'form-control', 'placeholder':' المسئول...', 'id':'admin'}),
        }
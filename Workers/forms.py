from datetime import datetime
from django import forms
from .models import *

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        exclude = ['deleted']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'image' : forms.FileInput(attrs={'class':'form-control'}),
            'phone' : forms.NumberInput(attrs={'class':'form-control'}),
            'work_type' : forms.Select(attrs={'class':'form-control'}),
            'day_cost' : forms.NumberInput(attrs={'class':'form-control'}),
        }
        

class WorkerDeleteForm(forms.ModelForm):
    class Meta:
        fields = ['deleted']
        model = Worker
        widgets = {
            'deleted' : forms.HiddenInput()
        }        
                
        
class WorkerPaymentForm(forms.ModelForm):
    class Meta:
        fields = ['date', 'price', 'worker', 'admin']
        model = WorkerPayment
        widgets = {
            'date' : forms.TextInput(attrs={'type':'date', 'class':'form-control',  'placeholder':'تاريخ السحب...', 'id':'date'}),
            'price' : forms.NumberInput(attrs={ 'class':'form-control', 'placeholder':'المبلغ...', 'id':'price'}),
            'admin' : forms.Select(attrs={'class':'form-control',  'placeholder':'المستلم...', 'id':'recipient', 'id':'admin'}),
        }
        
class WorkerPaymentReportForm(forms.Form):
    from_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date',
        'name':'form_date',
        'id':'from_date',
        'class':'form-control',
        'placeholder':'من ...'}),                       
        label= 'من',
        )
         
    to_date = forms.DateField(widget=forms.DateInput(attrs={
        'type':'date',
        'name':'to_date',
        'id':'to_date',
        'class':'form-control',
        'placeholder':'الي ...'}),
        label= 'الي',
        )     


class WorkerAttendanceForm(forms.ModelForm):
    class Meta:
        fields = ['date', 'hour_count']
        model = WorkerAttendance
        widgets = {
            'date' : forms.TextInput(attrs={'type':'date', 'class':'form-control',  'placeholder':'تاريخ السحب...', 'id':'date'}),
            'hour_count' : forms.Select(attrs={'class':'form-control',  'placeholder':'عدد الساعات...', 'id':'hours_count'}),
        }
        
        
   
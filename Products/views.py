import datetime
from django.db.models.aggregates import Sum
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import get_object_or_404, redirect , render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from django.views.generic import *

from Core.models import SystemInformation
from Products.forms import ProductDeleteForm, ProductForm
from .models import *


from django.contrib import messages
import weasyprint
from django.template.loader import render_to_string
from datetime import datetime, timedelta



# Create your views here.

class ProductList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
    paginate_by = 6
    template_name = 'Product/product_list.html'
    
    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة المنتجات'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    

class ProductTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Product
    paginate_by = 6
    template_name = 'Product/product_list.html'
    
    
    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class ProductCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductForm
    template_name = 'forms/product_form.html'
    success_url = reverse_lazy('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة منتج جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:ProductCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة منتج جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class ProductUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductForm
    template_name = 'forms/product_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل المنتج: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Products:ProductUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل المنتج " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url            
        
        

class ProductDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'
    

    def get_success_url(self):
        return reverse('Products:ProductList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل المنتج الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Products:ProductDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل المنتج " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())                



class ProductRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'
    

    def get_success_url(self):
        return reverse('Products:ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع منتج: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Products:ProductRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم المنتج " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())
    

class ProductSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductDeleteForm
    template_name = 'forms/product_form.html'

    def get_success_url(self):
        return reverse('Products:ProductTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المنتج: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Products:ProductSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المنتج " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Product.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())       
    
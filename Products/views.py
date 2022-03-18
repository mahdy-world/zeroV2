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
from .forms import *
from .models import *
from django.contrib import messages
import weasyprint
from django.template.loader import render_to_string
from datetime import datetime, timedelta


# Create your views here.

class ProductList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Product
    paginate_by = 4



    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة '
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    

class ProductTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Product
    paginate_by = 6
    
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
    form_class = ProductFormUpdate
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


class AddProductQuantity(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Product
    form_class = ProductQuantityForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة كمية للمنتج: ' + str(self.object)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:AddProductQuantity', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        myform = Product.objects.get(id=self.kwargs['pk'])
        myform.quantity += int(form.cleaned_data.get("add_quant"))
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request,  "تم اضافة كمية للمنتج " + str(self.object) + " بنجاح ", extra_tags="success")
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
        messages.success(self.request, " تم استرجاع المنتج " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
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


###################################################################


class SellerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = ProductSellers
    paginate_by = 6

    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة التجار'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class SellerTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = ProductSellers
    paginate_by = 6

    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class SellerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة تاجر جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:SellerCreate')
        return context

    def get_success_url(self):
        messages.success(self.request, "تم اضافة تاجر جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SellerUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerFormUpdate
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل التاجر: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Products:SellerUpdate', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, "تم تعديل التاجر " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class PaidSellerValue(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = SellerPayments
    form_class = ProductSellerPaymentForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استلام مبلغ من التاجر: ' + str(ProductSellers.objects.get(id=self.kwargs['pk']).name)
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Products:PaidSellerValue', kwargs={'pk': self.kwargs['pk']})
        return context

    def form_valid(self, form):
        seller = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform = SellerPayments()
        myform.seller = seller
        myform.paid_value = form.cleaned_data.get("paid_value")
        myform.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, "تم استلام مبلغ من التاجر " + str(ProductSellers.objects.get(id=self.kwargs['pk']).name) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url


class SellerDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل التاجر الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Products:SellerDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل التاجر " + str(self.object) + ' الي سلة المهملات بنجاح ', extra_tags="success")
        myform = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class SellerRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع تاجر: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Products:SellerRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع التاجر " + str(self.object) + ' الي القائمة بنجاح ', extra_tags="success")
        myform = ProductSellers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class SellerSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = ProductSellers
    form_class = ProductSellerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Products:SellerTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف التاجر: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Products:SellerSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف التاجر " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = ProductSellers.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())
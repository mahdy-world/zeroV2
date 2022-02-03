
from sys import int_info
from django.db.models.aggregates import Sum
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import get_object_or_404, redirect , render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib import messages


# Create your views here.
class FactoryList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Factory
    paginate_by = 6
    template_name = 'Factory/factory_list.html'
    
    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة المصانع'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context



class FactoryTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Factory
    paginate_by = 6
    template_name = 'Factory/factory_list.html'
    
    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('id')
        return queyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context



class FactoryCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'forms/factory_form.html'
    success_url = reverse_lazy('Factories:FactoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة مصنع جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Factories:FactoryCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة مصنع جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('SpareParts:SpareTypeList',)



class FactoryUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryForm
    template_name = 'forms/factory_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مصنع: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل المصنع " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
                


class FactoryDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/factory_form.html'
    

    def get_success_url(self):
        return reverse('Factories:FactoryList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل المصنع الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Factories:FactoryDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل المصنع " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Factory.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())        



class FactoryRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/factory_form.html'
    

    def get_success_url(self):
        return reverse('Factories:FactoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع مصنع: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Factories:FactoryRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم المصنع " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Factory.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())
    

class FactorySuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Factory
    form_class = FactoryDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Factories:FactoryTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نوع قطعة غيار بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Factories:FactorySuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المصنع " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Factory.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())    


class FactoryPayment(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_payment.html'
    
    def get_context_data(self, **kwargs):
        queryset = Payment.objects.filter(factory=self.object)
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        total_account =FactoryInSide.objects.filter(factory=self.object).aggregate(total=Sum('total_account')).get('total')
        total = ''
        if total_account and payment_sum != None:
            total = total_account - payment_sum
        
        
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('id')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوبات مصنع: ' + str(self.object)
        context['form'] = FactoryPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        return context
    
    
class FactoryPayment_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/payment_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = Payment.objects.filter(factory=self.object)
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        total_account =FactoryInSide.objects.filter(factory=self.object).aggregate(total=Sum('total_account')).get('total')
        total = ''
        if total_account and payment_sum != None:
            total = total_account - payment_sum
        
        
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('id')
        context['payment_sum'] = payment_sum
        context['total_account'] = total_account
        context['total'] = total
        context['title'] = 'مسحوبات مصنع: ' + str(self.object)
        context['form'] = FactoryPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        return context


class FactoryPaymentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Payment
    form_class = FactoryPaymentForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  مسحوبات يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Factories:FactoryPaymentUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل المحسوبات " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url




def FactoryPaymentCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id)
        
        date = request.POST.get('date')
        admin = request.POST.get('admin')
        user = User.objects.get(id=admin)
        recipient = request.POST.get('recipient')
        price = request.POST.get('price')
        
        if factory_id and date and admin and recipient and price:
            obj = Payment()
            obj.factory = factory
            obj.date = date
            obj.admin = user
            obj.recipient = recipient
            obj.price = price
            obj.save()
            
            if obj:
                response = {
                    'msg' : 1
                }
        else:
            response = {
                'msg' : 0
            }
        return JsonResponse(response)
    
    

    
    
def FactoryPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj =  Payment.objects.get(id=payment_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)



class FactoryOutside(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_outside.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['outSide'] = queryset.order_by('id')
        context['title'] = 'المستلم من المصنع: ' + str(self.object)
        context['sum_weight'] = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight_after'] = queryset.aggregate(after=Sum('weight_after_loss')).get('after')
        context['form'] = FactoryOutSideForm(self.request.POST or None)
        context['type'] = 'list'
        return context
    

class FactoryOutSide_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/outside_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['outSide'] = queryset.order_by('id')
        context['sum_weight'] = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight_after'] = queryset.aggregate(after=Sum('weight_after_loss')).get('after')
        return context    


def FactoryOutSideCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id)
        print(factory)
        date = request.POST.get('date')
        number = request.POST.get('number')
        weight = request.POST.get('weight')
        color = request.POST.get('color')
        percent_loss = request.POST.get('percent_loss')
        weight_after_loss = request.POST.get('weight_after_loss')
        admin = request.POST.get('admin')
        
        if factory_id and date and admin and number and weight and color and percent_loss and weight_after_loss:
            obj = FactoryOutSide()
            obj.factory = factory
            obj.date = date
            obj.admin = admin
            obj.number = number
            obj.weight = weight
            obj.color = color
            obj.percent_loss = percent_loss
            obj.weight_after_loss = weight_after_loss
            obj.save()
            
            if obj:
                response = {
                    'msg' : 1
                }
        else:
            response = {
                'msg' : 0
            }
        return JsonResponse(response)
        
          
    

           
    
def FactoryOutsideDelete(request):
    if request.is_ajax():
        outside_id = request.POST.get('outside_id')
        obj =  FactoryOutSide.objects.get(id=outside_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)
 

class FactoryInside(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_inside.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryInSide.objects.filter(factory=self.object)
        outSide = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['inSide'] = queryset.order_by('id')
        context['title'] = 'الخارج لمصنع: ' + str(self.object)
        context['form'] = FactoryInSideForm(self.request.POST or None)
        context['sum_outside'] = outSide.aggregate(out=Sum('weight_after_loss')).get('out')
        context['sum_weight'] = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight_after'] = queryset.aggregate(after=Sum('total_account')).get('after')
        context['type'] = 'list'
        return context


class FactoryInSide_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/inside_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = FactoryInSide.objects.filter(factory=self.object)
        outSide = FactoryOutSide.objects.filter(factory=self.object)
        context = super().get_context_data(**kwargs)
        context['inSide'] = queryset.order_by('id')
        context['sum_outside'] = outSide.aggregate(out=Sum('weight_after_loss')).get('out')
        context['sum_weight'] = queryset.aggregate(weight=Sum('weight')).get('weight')
        context['sum_weight_after'] = queryset.aggregate(after=Sum('total_account')).get('after')
        return context    


      
def FactoryInSideCreate(request):
    if request.is_ajax():
        factory_id = request.POST.get('id')
        factory = Factory.objects.get(id=factory_id) 
        print(factory)
        date = request.POST.get('date')
        weight = request.POST.get('weight')
        color = request.POST.get('color')
        product = request.POST.get('product')
        product_weight = request.POST.get('product_weight')
        product_time = request.POST.get('product_time')
        product_count = request.POST.get('product_count')
        hour_count = request.POST.get('hour_count')
        hour_price = request.POST.get('hour_price')
        total_account = request.POST.get('total_account')
        admin = request.POST.get('admin')
        
        if factory_id and date and weight and color and product and product_weight and product_count and product_time and hour_count and hour_price and total_account and admin:
    
            obj = FactoryInSide()
            obj.factory = factory
            obj.date = date
            obj.weight = weight
            obj.color = color
            obj.product = product
            obj.product_weight = product_weight
            obj.product_time = product_time
            obj.product_count = product_count
            obj.hour_count = hour_count
            obj.hour_price = hour_price
            obj.total_account = total_account
            obj.admin = admin
            obj.save()
        
            if obj:
                response = {
                'msg' : 1
                }
        else:
            response = {
                'msg' : 0
            }
        return JsonResponse(response)
        
           
    

def FactoryInsideDelete(request):
    if request.is_ajax():
        inside_id = request.POST.get('inside_id')
        obj =  FactoryInSide.objects.get(id=inside_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)    
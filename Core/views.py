from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import  get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from Core.forms import SystemInfoForm
from Machines.models import *
from Core.models import SystemInformation
from SpareParts.models import SparePartsOrders
from Factories.models import Factory

# Create your views here.


@login_required(login_url='Auth:login')
def Index(request):
    return render(request, 'core/index.html')



class SystemInfoCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = SystemInformation
    template_name = 'forms/form_template.html'
    form_class = SystemInfoForm
    success_url = reverse_lazy('Core:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'بيانات النظام'
        context['message'] = 'info'
        context['action_url'] = reverse_lazy('Core:SystemInfoCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم إضافة بيانات للنظام بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Core:index')
    
    
class SystemInfoUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SystemInformation
    template_name = 'forms/form_template.html'
    form_class = SystemInfoForm
    success_url = reverse_lazy('Core:index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل بيانات النظام'
        context['message'] = 'info'
        context['action_url'] = reverse_lazy('Core:SystemInfoUpdate',kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل بيانات النظام بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Core:index')
 
 
class MachineSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesNames
    template_name = 'Machines/machinesnames_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    
    def get_queryset(self):
        machine_search = self.request.GET.get("machine")  
        queryset = self.model.objects.filter(name__icontains=machine_search, deleted=False)
        return queryset
    
class FactorySearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Factory
    template_name = 'Factory/factory_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
    
    def get_queryset(self):
        search = self.request.GET.get("factory")  
        queryset = self.model.objects.filter(name__icontains=search, deleted=False)
        return queryset


class SparePartsSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = SparePartsNames
    template_name = 'SpareParts/sparepartsnames_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة انواع قطع الغيار'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['spare_search'] = self.request.GET.get("spare")
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        spare_search = self.request.GET.get("spare")
        queryset = self.model.objects.filter(name__icontains=spare_search, deleted=False)
        return queryset



class SparePartsOrderSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    template_name = 'SpareParts/sparepartsorders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['page'] = 'active'
        context['spare_order_search'] = self.request.GET.get("spareOrder_search")
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        spare_order_search = self.request.GET.get("spareOrder_search")
        queryset = self.model.objects.filter(order_number__icontains=spare_order_search, deleted=False)
        return queryset
    
    
    
class MachineOrderSearch(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesOrders
    template_name = 'Machines/machinesorders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['message'] = 'active'
        context['machine_order_search'] = self.request.GET.get("MachineOrder_search")
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        machine_order_search = self.request.GET.get("MachineOrder_search")
        queryset = self.model.objects.filter(order_number__icontains=machine_order_search, deleted=False)
        return queryset



def Read(request):
    if request.is_ajax():
        pk = request.POST.get('id')
        obj = MachineNotifecation.objects.get(id=pk)
        obj.read = True
        obj.save(update_fields=['read'])
        return HttpResponse('Updated')

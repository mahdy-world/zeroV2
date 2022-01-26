from django.db.models.aggregates import Sum
from django.shortcuts import get_object_or_404, redirect ,HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import *
from django.db.models import Count
from django.contrib import messages
from Machines.models import MachineNotifecation

from Treasury.models import WorkTreasuryTransactions
from datetime import datetime, timedelta
from .forms import *
from .models import *

# Create your views here.

# Spare Parts Type Module 
class SparePartsTypeList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    paginate_by = 12
    template_name = 'SpareParts/sparepartstypes_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة انواع قطع الغيار'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

class SparePartsTypeTrachList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    paginate_by = 12
    template_name = 'SpareParts/sparepartstypes_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

class SparePartsTypeCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    form_class = SparePartsTypeForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('SpareParts:SpareTypeList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة نوع قطعة غيار '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsTypeCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم إضافة نوع قطعة غيار بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('SpareParts:SpareTypeList',)

class SparePartsTypeUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    form_class = SparePartsTypeForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل نوع قطعة غيار: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsTypeUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  " تم تعديل نوع قطعة غيار " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('SpareParts:SpareTypeList',)

class SparePartsTypeDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    form_class = DeleteTypeForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SpareTypeList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل نوع قطعة غيار الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsTypeDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل نوع قطعة غيار " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = SparePartsTypes.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())

class SparePartsTypeRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    form_class = DeleteTypeForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SpareTypeTrachList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع نوع قطعة غيار: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsTypeRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع نوع قطعة غيار " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = SparePartsTypes.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())
    

class SparePartsTypeSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SparePartsTypes
    form_class = DeleteTypeForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('SpareParts:SpareTypeTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نوع قطعة غيار بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsTypeSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف نوع قطعة غيار " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsTypes.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())    

#-----------------------------------------------------------------------------------------------------------------------------------

# Spare Parts Names Module 
class SparePartsNameList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsNames
    paginate_by = 12
    template_name = 'SpareParts/sparepartsnames_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

class SparePartsNameTrachList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsNames
    paginate_by = 12
    template_name = 'SpareParts/sparepartsnames_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Name'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class SparePartsNameCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsNames
    form_class = SparePartsNameForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('SpareParts:SparePartsNameList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة صنف قطعة غيار '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsNameCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم اضافة صنف قطعة غيار بنجاح", extra_tags="success")
       
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
   
class SparePartsNameUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsNames
    form_class = SparePartsNameForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل صنف قطعة غيار: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsNameUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل صنف قطعة غيار " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('SpareParts:SparePartsNameList',)

class SparePartsNameDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsNames
    form_class = DeleteNameForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsNameList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل صنف قطعة غيار: ' + str(self.object) + 'الي سلة المهملات'
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsNameDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل صنف قطعة غيار " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = SparePartsNames.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())

class SparePartsNameRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsNames
    form_class = DeleteNameForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SpareNameTrachList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع صنف قطعة غيار: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsNameRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع صنف قطعة غيار " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = SparePartsNames.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())

class SparePartsNameSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SparePartsNames
    form_class = DeleteNameForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('SpareParts:SpareNameTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف صنف قطعة غيار بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsNameSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف صنف قطعة غيار " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsNames.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())   



# Spare Parts Warehouse Module 
class SparePartsWarehouseList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    paginate_by = 12
    template_name = 'SpareParts/sparepartswarehouse_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

class SparePartsWarehouseTrachList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    paginate_by = 12
    template_name = 'SpareParts/sparepartswarehouse_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Name'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

class SparePartsWarehouseCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    form_class = SparePartsWarehouseForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('SpareParts:SparePartsWarehouseList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مخزن قطع غيار '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsWarehouseCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم اضافة مخزن قطع غيار بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('SpareParts:SparePartsWarehouseList',)

class SparePartsWarehouseUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    form_class = SparePartsWarehouseForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مخزن قطع غيار: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsWarehouseUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم تعديل مخزن قطع غيار " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('SpareParts:SparePartsWarehouseList',)

class SparePartsWarehouseDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    form_class = WarehouseDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsWarehouseList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل مخزن قطع غيار : ' + str(self.object) + 'الي سلة المهملات'
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsWarehouseDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل مخزن قطع غيار " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = SparePartsWarehouses.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())

class SparePartsWarehouseRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    form_class = WarehouseDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsWarehouseTrachList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع مخزن قطع غيار: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsWarehouseRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع مخزن قطع غيار " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = SparePartsWarehouses.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())

class SparePartsWarehouseSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SparePartsWarehouses
    form_class = WarehouseDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsWarehouseTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مخزن قطع الغيار بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsWarehouseSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مخزن قطع الغيار " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsWarehouses.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url()) 
    


# Spare Parts Suppliers Module 
class SparePartsSupplierList(LoginRequiredMixin ,ListView):

    login_url = '/auth/login/'
    model = SparePartsSuppliers
    paginate_by = 12
    template_name = 'SpareParts/sparepartssuppliers_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context
  
  
    
class SparePartsSupplierTrachList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    paginate_by = 12
    template_name = 'SpareParts/sparepartssuppliers_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Name'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context





class SparePartsSupplierCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    form_class = SparePartSupplierForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('SpareParts:SparePartsSupplierList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مورد قطع غيار '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsSupplierCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "  تم اضافة مورد قطع غيار بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('SpareParts:SparePartsSupplierList',)
  
  
  
    
class SparePartsSupplierUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    form_class = SparePartSupplierForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مورد قطع غيار: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsSupplierUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم تعديل مورد قطع غيار " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('SpareParts:SparePartsSupplierList',)




class SparePartsSupplierDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsSupplierList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل مورد قطع غيار: ' + str(self.object) + 'الي سلة المهملات'
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsSupplierDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل مورد قطع غيار " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = SparePartsSuppliers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())



class SparePartsSupplierRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsSupplierTrachList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع مورد قطع غيار: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsSupplierRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع مورد قطع غيار " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = SparePartsSuppliers.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())



class SparePartsSupplierSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SparePartsSuppliers
    form_class = SupplierDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsSupplierTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مورد قطع الغيار : ' + str(self.object) + 'بشكل نهائي'
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsSupplierSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مورد قطع الغيار " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsSuppliers.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url()) 


# Spare Parts Orders Module 
class SparePartsOrderList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    paginate_by = 12
    template_name = 'SpareParts/sparepartsorders_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context



class SparePartsOrderTrachList(LoginRequiredMixin ,ListView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    paginate_by = 12
    template_name = 'SpareParts/sparepartsorders_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Name'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context



class SparePartsOrderCreate(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    form_class = SparePartOrderForm
    template_name = 'forms/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة طلبية قطع غيار '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderCreate')
        return context
    
    def form_valid(self, form):
        self.object = form.save()
        noti1 = MachineNotifecation()
        noti1.created_at = form.cleaned_data.get('order_deposit_date')
        noti1.spare_order = self.object
        noti1.notifeaction_type = 5
        noti1.message = "تنبية بشأن..موعد دفع عربون طلب قطع غيار رقم : " + str(self.object)
        noti1.save()
        
        noti2 = MachineNotifecation()
        noti2.created_at = form.cleaned_data.get('order_rest_date')
        noti2.spare_order = self.object
        noti2.notifeaction_type = 6
        noti2.message = "تنبية بشأن..موعد دفع باقي عربون طلب قطع غيار رقم : " + str(self.object)
        noti2.save()
        
        
        noti3 = MachineNotifecation()
        noti3.created_at = form.cleaned_data.get('order_receipt_date')
        noti3.spare_order = self.object
        noti3.notifeaction_type = 7
        noti3.message = "اتنبية بشأن..موعد استلام البضاعة الخاصة بطلب قطع غيار رقم : " + str(self.object)
        noti3.save()
        
        return super().form_valid(form)
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, "  تم اضافة طلبية قطع غيار بنجاح", extra_tags="success")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.object.id})



class SparePartsOrderUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrders

    def get_form_class(self, **kwargs):
        op1 = SparePartsOrderOperations.objects.filter(order_number=self.object, operation_type=1)
        op2 = SparePartsOrderOperations.objects.filter(order_number=self.object, operation_type=2)
        if op2:
            form_class_name = SparePartOrderFormOp2
        elif op1:
            form_class_name = SparePartOrderFormOp1
        else:
            form_class_name = SparePartOrderForm
        return form_class_name

    # form_class = SparePartOrderForm
    template_name = 'forms/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل طلبية قطع غيار: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderUpdate', kwargs={'pk': self.object.id})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        op1 = SparePartsOrderOperations.objects.filter(order_number=self.object, operation_type=1)
        op2 = SparePartsOrderOperations.objects.filter(order_number=self.object, operation_type=2)
        if op1 or op2:
            form.fields['order_supplier'].queryset = SparePartsSuppliers.objects.filter(id=self.object.order_supplier.id)
        return form
    
    def get_success_url(self,**kwargs):
        messages.success(self.request, "تم تعديل طلبية قطع غيار رقم " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('SpareParts:SparePartsOrderList')

    def form_valid(self, form):
        date1 = form.cleaned_data.get("order_deposit_date") # تاريخ دفع العربون الحديث
        date2 = form.cleaned_data.get("order_rest_date") # تاريخ دفع باقي العربون الحديث
        date3 = form.cleaned_data.get("order_receipt_date") # تاريخ استلام البضاعة الحديث
        self.object = form.save()
        
        
        noti1 = MachineNotifecation.objects.get(spare_order = self.object, notifeaction_type = 5 ) # اشعار دفع العربون 
        noti2 = MachineNotifecation.objects.get(spare_order = self.object, notifeaction_type = 6 ) # اشعار دفع باقي المبلغ 
        noti3 = MachineNotifecation.objects.get(spare_order = self.object, notifeaction_type = 7 ) # اشعار استلام البضاعة 
        
        noti_date1 = noti1.created_at # تاريخ اشعار دفع العربون القديم
        noti_date2 = noti2.created_at # تاريخ اشعار دفع باقي العربون القديم
        noti_date3 = noti3.created_at # تاريخ اشعار استلام البضاعة القديم 
        
        
        if noti_date1 != date1 :
            noti1.created_at = form.cleaned_data.get("order_deposit_date")
            if noti1.read == True :
               noti1.read = False
               noti1.save()
               return redirect(self.get_success_url())
            noti1.save()
            return redirect(self.get_success_url())   
           
        elif noti_date2 != date2:
            noti2.created_at = form.cleaned_data.get("order_rest_date")
            if noti2.read == True :
                noti2.read = False
                noti2.save()
                return redirect(self.get_success_url())
            noti2.save()    
            return redirect(self.get_success_url())
        
        elif noti_date3 != date3:
            noti3.created_at = form.cleaned_data.get("order_receipt_date")
            if noti3.read == True :
                noti3.read = False
                noti3.save()
                return redirect(self.get_success_url())
            noti3.save()    
            return redirect(self.get_success_url())
        
        return redirect(self.get_success_url())  

class SparePartsOrderDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    form_class = OrderDeleteForm
    template_name = 'forms/order_form.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsOrderList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل طلبية قطع غيار الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل طلبية قطع غيار " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = SparePartsOrders.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())



class SparePartsOrderRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    form_class = OrderDeleteForm
    template_name = 'forms/order_form.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsOrderTrachList',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع طلبية قطع غيار: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع طلبية قطع غيار " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = SparePartsOrders.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())    


class SparePartsOrderSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrders
    form_class = OrderDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsOrderTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف طلبية قطع الغيار : ' + str(self.object.order_number) + 'بشكل نهائي'
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف طلبية قطع الغيار " + str(self.object.order_number) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsOrders.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url()) 



def SparePartsOrderDetail(request, pk):
    order = get_object_or_404(SparePartsOrders , id=pk)
    product = SparePartsOrderProducts.objects.all().filter(product_order=order,)
    
    count_product = SparePartsOrderProducts.objects.all().filter(product_order=order).count()

    queryset = SparePartsOrderProducts.objects.all().filter(product_order=order,)
    total = queryset.aggregate(total=Sum('product_price')).get('total')
    quantity = queryset.aggregate(quantity=Sum('product_quantity')).get('quantity')
    
    op1 = SparePartsOrderOperations.objects.filter(order_number=order, operation_type=1)
    op2 = SparePartsOrderOperations.objects.filter(order_number=order, operation_type=2)
    op3 = SparePartsOrderOperations.objects.filter(order_number=order, operation_type=3)
    op4 = SparePartsOrderOperations.objects.filter(order_number=order, operation_type=4)
    op5 = SparePartsOrderOperations.objects.filter(order_number=order, operation_type=5)

    if op4:
        op_4 = SparePartsOrderOperations.objects.get(order_number=order, operation_type=4)
        op_4_date = op_4.operation_date
        op_5_date = op_4_date + timedelta(days=30)
    else:
        op_5_date = order.order_receipt_date

    form = orderProductForm
    type_page = "list"
    page = "active"
    action_url = reverse_lazy('SpareParts:AddProductOrder',kwargs={'pk':order.id})
    
    context = {
        'order' : order,
        'type' : type_page,
        'page' : page,
        'form' : form,
        'action_url' : action_url,
        'product':product,
        'count_product':count_product,
        'total' :total,
        'op1':op1,
        'op2':op2,
        'op3':op3, 
        'op4':op4,
        'op5':op5,
        'qu':quantity,
        'date': datetime.now().date(),
        'op_5_date': op_5_date,

    }
    return render(request, 'SpareParts/sparepartsorders_detail.html', context)



def AddProductOrder(request, pk):
    order = get_object_or_404(SparePartsOrders , id=pk)
    product = SparePartsOrderProducts.objects.filter(product_order=order).order_by('id')
    count_product = SparePartsOrderProducts.objects.all().filter(product_order=order).count()
    print(count_product)
    
    form = orderProductForm(request.POST or None)
    type_page = "list"
    page = "active"
    action_url = reverse_lazy('SpareParts:AddProductOrder',kwargs={'pk':order.id})
    messages.success(request, " تم اضافة منتج الي الطلبية بنجاح ", extra_tags="success")

    context = {
        'order' : order,
        'type' : type_page,
        'page' : page,
        'form' : orderProductForm,
        'action_url' : action_url,
        'product':product,
        'count_product' : count_product
    }    
   
    if form.is_valid():
        obj = form.save(commit=False)
        obj.product_order = order 
        obj.save()
        return redirect('SpareParts:SparePartsOrderDetail', pk=order.id)
    
    
    return render(request, 'SpareParts/sparepartsorders_detail.html', context)        




class SparePartsOrderAddProductUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrderProducts
    form_class = orderProductForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل منتج داخل الطلبية: ' + str(self.object.product_name)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderAddProductUpdate', kwargs={'pk': self.object.id, 'id': self.object.product_order.id})
        return context
    
    def get_success_url(self,**kwargs):
        messages.success(self.request, "تم تعديل المنتج " + str(self.object.product_name) + " بنجاح ", extra_tags="success")

        # if self.request.POST.get('url'):
        #     return self.request.POST.get('url')
        # else:
        #     return self.success_url
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk': self.kwargs['id']})



class SparePartsOrderAddProductDelete(LoginRequiredMixin,UpdateView):
    login_url = '/auth/login/'
    model = SparePartsOrderProducts
    form_class = orderProductDeleteForm
    template_name = 'forms/form_template.html'
    
    def get_success_url(self):
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['id']})
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف منتج داخل الطلبية: ' + str(self.object.product_name)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOrderAddProductDelete', kwargs={'pk': self.object.id, 'id': self.object.product_order.id})
        return context
    

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المنتج " + str(self.object.product_name) + " نهائيا بنجاح ", extra_tags="success")
        my_form = SparePartsOrderProducts.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())
        



# عملية دفع العربون
class SparePartsOperationCreateDeposit(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrderOperations
    form_class = OperationForm
    template_name = 'forms/form_template.html'


    def get_success_url(self):
        messages.success(self.request, " تم دفع العربون بنجاح " , extra_tags="success")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع العربون .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk': self.kwargs['pk']})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع عربون '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOperationCreateDeposit', kwargs={'pk':self.kwargs['pk']})
        return context
    
    def get_form(self, *args, **kwargs):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        form = super(SparePartsOperationCreateDeposit, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = order_number.order_deposit_value
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        
        # اضافة في جدول عملية دفع العربون
        if float(treasury_balance) >= float(operation_value):
            myform = SparePartsOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 1
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()
        
            # خصم قيمة العربون من الخزنة 
            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])   
            
            # اضافة في جدول عمليات الخزنة 
            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع قيمة عربون طلبية رقم' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1 
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            
            notification = MachineNotifecation.objects.get(spare_order=order_number, notifeaction_type=5)
            notification.delete()
            print("delete_done")
            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())
        
        
        
#عملية باقي المبلغ 
class SparePartsOperationCreateReset(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrderOperations
    form_class = OperationForm
    template_name = 'forms/form_template.html'


    def get_success_url(self):
        messages.success(self.request, " تم دفع باقي المبلغ بنجاح " , extra_tags="success")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع باقي المبلغ .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع باقي المبلغ المستحق'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOperationCreateReset', kwargs={'pk':self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        order_products_val = SparePartsOrderProducts.objects.filter(product_order__id=self.kwargs['pk']).aggregate(sum=Sum('product_price')).get('sum')
        form = super(SparePartsOperationCreateReset, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = float(order_products_val) - float(order_number.order_deposit_value)
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        
        # اضافة في جدول عملية  الطلب
        if float(treasury_balance) >= float(operation_value):
            myform = SparePartsOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 2
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()
        
            # خصم قيمة باقي المبلغ من الخزنة 
            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])   
            
            # اضافة في جدول عمليات الخزنة 
            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع باقي مبلغ طلبية رقم' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1 
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            
            notification = MachineNotifecation.objects.get(spare_order=order_number, notifeaction_type=6)
            notification.delete()
            print("delete_done")
            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())
        

# عملية تخليص البضاعة         
class SparePartsOperationCreateClearance(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrderOperations
    form_class = OperationsForm3
    template_name = 'forms/form_template.html'


    def get_success_url(self):
        messages.success(self.request, " تم دفع مبلغ تخليص البضاعة بنجاح " , extra_tags="success")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع مبلغ تخليص البضاعة .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع مبلغ تخليص البضاعة '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOperationCreateClearance', kwargs={'pk':self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(SparePartsOperationCreateClearance, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = 1.0
        form.fields['operation_date'].initial = datetime.now().date()
        return form


    def form_valid(self, form):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        
        # اضافة في جدول عملية  الطلب
        if float(treasury_balance) >= float(operation_value):
            myform = SparePartsOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 3
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()
        
            # خصم قيمة باقي المبلغ من الخزنة 
            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])   
            
            # اضافة في جدول عمليات الخزنة 
            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع باقي مبلغ طلبية رقم' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1 
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())        
  
  
   

# عملية ضرائب البضاعة
class SparePartsOperationCreateTax(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrderOperations
    form_class = OperationsForm3
    template_name = 'forms/form_template.html'


    def get_success_url(self):
        messages.success(self.request, " تم دفع مبلغ ضرائب البضاعة بنجاح " , extra_tags="success")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع مبلغ ضرائب البضاعة .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع ضرائب البضاعة '
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOperationCreateTax', kwargs={'pk':self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(SparePartsOperationCreateTax, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = 1.0
        form.fields['operation_date'].initial = datetime.now().date()
        return form


    def form_valid(self, form):
        order_number = get_object_or_404(SparePartsOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")

        # اضافة في جدول عملية  الطلب
        if float(treasury_balance) >= float(operation_value):
            myform = SparePartsOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 5
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()

            # خصم قيمة باقي المبلغ من الخزنة
            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])

            # اضافة في جدول عمليات الخزنة
            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع مبلغ ضرائب طلبية رقم' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            
            notification = MachineNotifecation.objects.get(spare_order=order_number, notifeaction_type=8)
            notification.delete()
            print("delete_done")
            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())



#عملية استلام  البضاعة


class SparePartsOperationCreateOrder(LoginRequiredMixin ,CreateView):
    login_url = '/auth/login/'
    model = SparePartsOrderOperations
    form_class = OperationsForm2
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('SpareParts:SparePartsOrderDetail', kwargs={'pk':self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استلام البضاعة' 
        context['message'] = 'operation'
        context['action_url'] = reverse_lazy('SpareParts:SparePartsOperationCreateOrder', kwargs={'pk':self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(SparePartsOperationCreateOrder, self).get_form(*args, **kwargs)
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        messages.success(self.request, " تمت العملية بنجاح " , extra_tags="success")
        order_number = get_object_or_404(SparePartsOrders , id=self.kwargs['pk'])
        myform = SparePartsOrderOperations()
        myform.order_number = order_number
        myform.operation_type=4
        myform.warehouse_name = form.cleaned_data.get("warehouse_name")
        myform.operation_date = form.cleaned_data.get("operation_date")
        myform.save()
        
        
        # to delete notification for machine order operation
        notification = MachineNotifecation.objects.get(spare_order=order_number, notifeaction_type=7)
        notification.delete()
        print("delete_done")
        
        
        

        op_4 = SparePartsOrderOperations.objects.get(order_number=order_number, operation_type=4)
        op_4_date = op_4.operation_date
        op_5_date = op_4_date + timedelta(days=25)
        
        notification2 = MachineNotifecation()  
        notification2.created_at = op_5_date  
        notification2.spare_order = order_number
        notification2.notifeaction_type = 8
        notification2.message = "تنبية بشأن...موعد دفع ضرائب طلب قطع غيار رقم : " + str(order_number)
        notification2.save()        

        
        
        order_products = SparePartsOrderProducts.objects.filter(product_order=order_number, deleted=0)
        order_products_quantity = order_products.aggregate(count=Sum('product_quantity')).get('count')
        order_op3 = SparePartsOrderOperations.objects.get(order_number=order_number, operation_type=3)
        order_one_product_op3_cost = float(order_op3.operation_value) / float(order_products_quantity)
        for product in order_products:
            price_cost = (float(product.product_price) / float(product.product_quantity)) + float(order_one_product_op3_cost)
            transactions_filter = SparePartsWarehouseTransactions.objects.filter(item=product.product_name, warehouse=form.cleaned_data.get("warehouse_name"), price_cost=price_cost)
            if transactions_filter:
                transaction = SparePartsWarehouseTransactions.objects.get(item=product.product_name, warehouse=form.cleaned_data.get("warehouse_name"), price_cost=price_cost)
                transaction.quantity += product.product_quantity
                transaction.save(update_fields=['quantity'])
            else:
                transaction = SparePartsWarehouseTransactions()
                transaction.warehouse = form.cleaned_data.get("warehouse_name")
                transaction.item = product.product_name
                transaction.quantity = product.product_quantity
                transaction.price_cost = price_cost
                transaction.save()

        return redirect(self.get_success_url())   
    

# عرض تفاصيل المخزن


class SparePartsWarehouseDetail(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = SparePartsWarehouseTransactions
    template_name = 'SpareParts/sparepartswharehouse_detail.html'
    # paginate_by = 10
    
    def get_queryset(self):
        queryset = SparePartsWarehouseTransactions.objects.filter(warehouse=self.kwargs['pk']).order_by('item')
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'المخزون الخاص بمخزن قطع الغيار: ' + str(SparePartsWarehouses.objects.get(id=int(self.kwargs['pk'])).name)
        context['type'] = 'list'
        context['count'] = SparePartsWarehouseTransactions.objects.filter(warehouse=self.kwargs['pk']).order_by('warehouse').count()
        
        return context
    
    
class SparePartsNamesDetail(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = SparePartsWarehouseTransactions
    template_name = 'SpareParts/sparepartsnames_detail.html'
    # paginate_by = 10
    
    def get_queryset(self):
        queryset = SparePartsWarehouseTransactions.objects.filter(item=self.kwargs['pk']).order_by('warehouse')
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'المخزون الخاص بقطعة الغيار: ' + str(self.kwargs['name'])
        context['type'] = 'list'
        context['count'] = SparePartsWarehouseTransactions.objects.filter(item=self.kwargs['pk']).order_by('warehouse').count()
        
        return context
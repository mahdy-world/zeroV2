from django.db.models import Sum, Count, query
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import *
from .models import *
from .forms import *
from django.contrib import messages
from datetime import datetime, timedelta


# Create your views here.
class TypesActiveList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesTypes
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset


class TypesTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesTypes
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset


class TypesCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesTypes
    form_class = MachinesTypesForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة نوع ماكينة '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:types_create')
        return context

    def get_success_url(self):
        messages.success(self.request, "  تم إضافة نوع ماكينة بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Machines:types_active_list')

    # def get_success_url(self):
    #     if self.request.POST.get('url'):
    #         return self.request.POST.get('url')
    #     else:
    #         return self.success_url


class TypesUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesTypes
    form_class = MachinesTypesForm
    template_name = 'forms/form_template.html'
    # success_url = reverse_lazy('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل نوع ماكينة: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:types_update', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, " تم تعديل نوع ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('Machines:types_active_list')


class TypesDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesTypes
    form_class = MachinesTypesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نوع ماكينة: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Machines:types_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف نوع ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesTypes.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 1
        my_form.save()
        return redirect(self.get_success_url())


class TypesRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesTypes
    form_class = MachinesTypesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:types_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ارجاع نوع ماكينة: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Machines:types_restore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع نوع ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesTypes.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 0
        my_form.save()
        return redirect(self.get_success_url())


class TypesSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesTypes
    form_class = MachinesTypesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:types_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف نوع ماكينة بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:types_super_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف نوع ماكينة " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = MachinesTypes.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


################################################################


class WarehousesActiveList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset


class WarehousesTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset


class WarehousesCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    form_class = MachinesWarehousesForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Machines:warehouses_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مخزن ماكينات '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:warehouses_create')
        return context

    def get_success_url(self):
        messages.success(self.request, "  تم إضافة مخزن ماكينات بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Machines:warehouses_active_list')

    # def get_success_url(self):
    #     if self.request.POST.get('url'):
    #         return self.request.POST.get('url')
    #     else:
    #         return self.success_url


class WarehousesUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    form_class = MachinesWarehousesForm
    template_name = 'forms/form_template.html'
    # success_url = reverse_lazy('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مخزن ماكينات: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:warehouses_update', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, " تم تعديل مخزن ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('Machines:warehouses_active_list')


class WarehousesDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    form_class = MachinesWarehousesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:warehouses_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مخزن ماكينات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Machines:warehouses_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مخزن ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesWarehouses.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 1
        my_form.save()
        return redirect(self.get_success_url())


class WarehousesRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    form_class = MachinesWarehousesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:warehouses_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ارجاع مخزن ماكينات: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Machines:warehouses_restore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع مخزن ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesWarehouses.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 0
        my_form.save()
        return redirect(self.get_success_url())


class WarehousesSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesWarehouses
    form_class = MachinesWarehousesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:warehouses_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مخزن ماكينات بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:warehouses_super_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مخزن ماكينات " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = MachinesWarehouses.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


################################################################


class NamesActiveList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesNames
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset


class NamesTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesNames
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset


class NamesCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesNames
    form_class = MachinesNamesForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Machines:names_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة صنف ماكينة '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:names_create')
        return context

    def get_success_url(self):
        messages.success(self.request, "  تم إضافة صنف ماكينة بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Machines:names_active_list')

    # def get_success_url(self):
    #     if self.request.POST.get('url'):
    #         return self.request.POST.get('url')
    #     else:
    #         return self.success_url


class NamesUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesNames
    form_class = MachinesNamesForm
    template_name = 'forms/form_template.html'
    # success_url = reverse_lazy('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل صنف ماكينة: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:names_update', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, " تم تعديل صنف ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('Machines:names_active_list')


class NamesDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesNames
    form_class = MachinesNamesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:names_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف صنف ماكينة: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Machines:names_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف صنف ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesNames.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 1
        my_form.save()
        return redirect(self.get_success_url())
    

class NamesDetail(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = WarehouseTransactions
    template_name = 'Machines/machinesnames_detail.html'
    # paginate_by = 5
    
    def get_queryset(self):
        queryset = WarehouseTransactions.objects.filter(item=self.kwargs['pk']).order_by('warehouse')
        return queryset
    
    
    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'تفاصيل المخزون الخاص بالماكينة: ' + str(self.kwargs['name'])
        context['type'] = 'list'
        context['machine'] = MachinesNames.objects.get(id=int(self.kwargs['pk']))
        context['count'] = WarehouseTransactions.objects.filter(item=self.kwargs['pk']).order_by('warehouse').count()
        
        return context
        
    


class NamesRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesNames
    form_class = MachinesNamesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:names_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ارجاع صنف ماكينة: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Machines:names_restore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع صنف ماكينة " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesNames.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 0
        my_form.save()
        return redirect(self.get_success_url())


class NamesSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesNames
    form_class = MachinesNamesFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:names_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف صنف ماكينة بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:names_super_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف صنف ماكينة " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = MachinesNames.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


################################################################


class SuppliersActiveList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('id')
        return queryset


class SuppliersTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('id')
        return queryset


class SuppliersCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    form_class = MachinesSuppliersForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Machines:suppliers_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة مورد ماكينات '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:suppliers_create')
        return context

    def get_success_url(self):
        messages.success(self.request, "  تم إضافة مورد ماكينات بنجاح", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        # return reverse('Machines:suppliers_active_list')

    # def get_success_url(self):
    #     if self.request.POST.get('url'):
    #         return self.request.POST.get('url')
    #     else:
    #         return self.success_url


class SuppliersUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    form_class = MachinesSuppliersForm
    template_name = 'forms/form_template.html'
    # success_url = reverse_lazy('Machines:types_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل مورد ماكينات: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:suppliers_update', kwargs={'pk': self.object.id})
        return context

    def get_success_url(self):
        messages.success(self.request, " تم تعديل مورد ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        return reverse('Machines:suppliers_active_list')


class SuppliersDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    form_class = MachinesSuppliersFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:suppliers_active_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مورد ماكينات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Machines:suppliers_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مورد ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesSuppliers.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 1
        my_form.save()
        return redirect(self.get_success_url())


class SuppliersRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    form_class = MachinesSuppliersFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:suppliers_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ارجاع مورد ماكينات: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Machines:suppliers_restore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم ارجاع مورد ماكينات " + str(self.object) + " بنجاح ", extra_tags="success")
        my_form = MachinesSuppliers.objects.get(id=self.kwargs['pk'])
        my_form.deleted = 0
        my_form.save()
        return redirect(self.get_success_url())


class SuppliersSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesSuppliers
    form_class = MachinesSuppliersFormDelete
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:suppliers_trash_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف مورد ماكينات بشكل نهائي: ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:suppliers_super_delete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف مورد ماكينات " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = MachinesSuppliers.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


###################################################################
###################################################################


class MachinesOrdersList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesOrders
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=False).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class MachinesOrdersTrashList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = MachinesOrders
    paginate_by = 12

    def get_queryset(self):
        queryset = self.model.objects.filter(deleted=True).order_by('-id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'trash'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class MachinesOrdersCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrders
    form_class = MachinesOrdersForm
    template_name = 'forms/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'إضافة طلبية مكن'
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrdersCreate')
        return context
    
    
    def form_valid(self, form):
        self.object = form.save()
        noti1 = MachineNotifecation()
        noti1.created_at = form.cleaned_data.get('order_deposit_date')
        noti1.machine_order = self.object
        noti1.notifeaction_type = 1
        noti1.message = "تنبية بشأن..موعد دفع عربون طلب مكينات رقم : " + str(self.object)
        noti1.save()
        
        noti2 = MachineNotifecation()
        noti2.created_at = form.cleaned_data.get('order_rest_date')
        noti2.machine_order = self.object
        noti2.notifeaction_type = 2
        noti2.message = "تنبية بشأن..موعد دفع باقي عربون طلب مكينات رقم : " + str(self.object)
        noti2.save()
        
        
        noti3 = MachineNotifecation()
        noti3.created_at = form.cleaned_data.get('order_receipt_date')
        noti3.machine_order = self.object
        noti3.notifeaction_type = 3
        noti3.message = "اتنبية بشأن..موعد استلام البضاعة الخاصة بطلب مكينات رقم : " + str(self.object)
        noti3.save()
        
        return super().form_valid(form)
        
        
    def get_success_url(self, **kwargs):
        messages.success(self.request, "  تم اضافة طلبية مكن بنجاح", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.object.id})

        
    

class MachinesOrdersUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrders

    def get_form_class(self, **kwargs):
        op1 = MachinesOrderOperations.objects.filter(order_number=self.object, operation_type=1)
        op2 = MachinesOrderOperations.objects.filter(order_number=self.object, operation_type=2)
        if op2:
            form_class_name = MachinesOrdersFormOp2
        elif op1:
            form_class_name = MachinesOrdersFormOp1
        else:
            form_class_name = MachinesOrdersForm
        return form_class_name

    template_name = 'forms/order_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل طلبية مكن: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:MachinesOrdersUpdate', kwargs={'pk': self.object.id})
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class=self.form_class)
        op1 = MachinesOrderOperations.objects.filter(order_number=self.object, operation_type=1)
        op2 = MachinesOrderOperations.objects.filter(order_number=self.object, operation_type=2)
        if op1 or op2:
            form.fields['order_supplier'].queryset = MachinesSuppliers.objects.filter(
                id=self.object.order_supplier.id)
        return form
    
    def get_success_url(self, **kwargs):
        messages.success(self.request, " تم تعديل طلبية مكن " + str(self.object) + " بنجاح ", extra_tags="info")
        return reverse('Machines:MachinesOrdersList')
    
    def form_valid(self, form):
        date1 = form.cleaned_data.get("order_deposit_date") # تاريخ دفع العربون الحديث
        date2 = form.cleaned_data.get("order_rest_date") # تاريخ دفع باقي العربون الحديث
        date3 = form.cleaned_data.get("order_receipt_date") # تاريخ استلام البضاعة الحديث
        self.object = form.save()
        
        
        noti1 = MachineNotifecation.objects.get(machine_order = self.object, notifeaction_type = 1 ) # اشعار دفع العربون 
        noti2 = MachineNotifecation.objects.get(machine_order = self.object, notifeaction_type = 2 ) # اشعار دفع باقي المبلغ 
        noti3 = MachineNotifecation.objects.get(machine_order = self.object, notifeaction_type = 3 ) # اشعار استلام البضاعة 
        
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
        
    


class MachinesOrdersDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrders
    form_class = MachinesOrdersDeleteForm
    template_name = 'forms/order_form.html'

    def get_success_url(self):
        return reverse('Machines:MachinesOrdersList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف طلبية مكن: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Machines:MachinesOrdersDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف طلبية مكن " + str(self.object) + ' بنجاح ', extra_tags="danger")
        myform = MachinesOrders.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())


class MachinesOrdersRestore(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrders
    form_class = MachinesOrdersDeleteForm
    template_name = 'forms/order_form.html'

    def get_success_url(self):
        return reverse('Machines:MachinesOrdersTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع طلبية مكن: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Machines:MachinesOrdersRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم استرجاع طلبية مكن " + str(self.object) + ' بنجاح ', extra_tags="dark")
        myform = MachinesOrders.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class MachinesOrdersSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrders
    form_class = MachinesOrdersDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:MachinesOrdersTrashList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف طلبية مكن : ' + str(self.object.order_number) + 'بشكل نهائي'
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:MachinesOrdersSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف طلبية مكن " + str(self.object.order_number) + " نهائيا بنجاح ",
                         extra_tags="success")
        my_form = MachinesOrders.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


###################################################################


def  MachinesOrdersDetail(request, pk):
    order = get_object_or_404(MachinesOrders, id=pk)
    product = MachinesOrderProducts.objects.filter(product_order=order).order_by('id')
    count_product = product.count()

    total = product.aggregate(total=Sum('product_price')).get('total')
    quantity = product.aggregate(quantity=Sum('product_quantity')).get('quantity')

    op1 = MachinesOrderOperations.objects.filter(order_number=order, operation_type=1)
    op2 = MachinesOrderOperations.objects.filter(order_number=order, operation_type=2)
    op3 = MachinesOrderOperations.objects.filter(order_number=order, operation_type=3)
    op4 = MachinesOrderOperations.objects.filter(order_number=order, operation_type=4)
    op5 = MachinesOrderOperations.objects.filter(order_number=order, operation_type=5)

    if op4:
        op_4 = MachinesOrderOperations.objects.get(order_number=order, operation_type=4)
        op_4_date = op_4.operation_date
        op_5_date = op_4_date + timedelta(days=30)
    else:
        op_5_date = order.order_receipt_date

    form = MachinesOrderProductsForm
    type_page = "list"
    page = "active"
    action_url = reverse_lazy('Machines:AddProductOrder', kwargs={'pk': order.id})

    context = {
        'order': order,
        'type': type_page,
        'page': page,
        'form': form,
        'action_url': action_url,
        'product': product,
        'count_product': count_product,
        'total': total,
        'op1': op1,
        'op2': op2,
        'op3': op3,
        'op4': op4,
        'op5': op5,
        'qu': quantity,
        'date': datetime.now().date(),
        'op_5_date': op_5_date,

    }
    return render(request, 'Machines/machinesorders_detail.html', context)


def AddProductOrder(request, pk):
    order = get_object_or_404(MachinesOrders, id=pk)
    product = MachinesOrderProducts.objects.filter(product_order=order).order_by('id')
    count_product = product.count()

    form = MachinesOrderProductsForm(request.POST or None)
    type_page = "list"
    page = "active"
    action_url = reverse_lazy('Machines:AddProductOrder', kwargs={'pk': order.id})
    messages.success(request, " تم اضافة منتج الي الطلبية بنجاح ", extra_tags="success")

    context = {
        'order': order,
        'type': type_page,
        'page': page,
        'form': MachinesOrderProductsForm,
        'action_url': action_url,
        'product': product,
        'count_product': count_product
    }

    if form.is_valid():
        obj = form.save(commit=False)
        obj.product_order = order
        obj.save()
        return redirect('Machines:MachinesOrdersDetail', pk=order.id)

    return render(request, 'Machines/machinesorders_detail.html', context)


class MachinesOrderProductsUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrderProducts
    form_class = MachinesOrderProductsForm
    template_name = 'forms/form_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل المنتج: ' + str(self.object.product_name)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderProductsUpdate',
                                             kwargs={'pk': self.object.id, 'id': self.object.product_order.id})
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, " تم تعديل منتج " + str(self.object.product_name) + " بنجاح ", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['id']})


class MachinesOrderProductsDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = MachinesOrderProducts
    form_class = MachinesOrderProductsDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف المنتج: ' + str(self.object.product_name)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderProductsDelete',
                                             kwargs={'pk': self.object.id, 'id': self.object.product_order.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف المنتج " + str(self.object.product_name) + " من الفاتورة بنجاح ",
                         extra_tags="success")
        my_form = MachinesOrderProducts.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())


###################################################################


class MachinesOrderOperationsCreateDeposit(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrderOperations
    form_class = MachinesOrderOperationsForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        messages.success(self.request, " تم دفع العربون بنجاح ", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع العربون .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'دفع عربون'
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderOperationsCreateDeposit', kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        form = super(MachinesOrderOperationsCreateDeposit, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = order_number.order_deposit_value
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        if float(treasury_balance) >= float(operation_value):
            myform = MachinesOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 1
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()

            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])

            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع قيمة عربون طلبية رقم ' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            
            notification = MachineNotifecation.objects.get(machine_order=order_number, notifeaction_type=1)
            notification.delete()
            print("delete_done")

            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())


class MachinesOrderOperationsCreateReset(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrderOperations
    form_class = MachinesOrderOperationsForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        messages.success(self.request, " تم دفع باقي المبلغ المستحق بنجاح ", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع باقي المبلغ المستحق .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع باقي المبلغ '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderOperationsCreateReset',
                                             kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        order_products_val = MachinesOrderProducts.objects.filter(product_order__id=self.kwargs['pk']).aggregate(sum=Sum('product_price')).get('sum')
        form = super(MachinesOrderOperationsCreateReset, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = float(order_products_val) - float(order_number.order_deposit_value)
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        if float(treasury_balance) >= float(operation_value):
            myform = MachinesOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 2
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()

            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])

            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع باقي مبلغ طلبية رقم ' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()

            # to delete notification for Machines Order Operations Create Reset
            notification = MachineNotifecation.objects.get(machine_order=order_number, notifeaction_type=2)
            notification.delete()
            print("delete_done")
            
            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())


class MachinesOrderOperationsCreateClearance(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrderOperations
    form_class = MachinesOrderOperationsForm3
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        messages.success(self.request, " تم دفع مبلغ تخليص البضاعة بنجاح ", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع مبلغ تخليص البضاعة .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع مبلغ تخليص البضاعة '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderOperationsCreateClearance',
                                             kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(MachinesOrderOperationsCreateClearance, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = 1.0
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        if float(treasury_balance) >= float(operation_value):
            myform = MachinesOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 3
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()

            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])

            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع مبلغ تخليص بضاعة طلبية رقم ' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()

            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())


class MachinesOrderOperationsCreateTax(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrderOperations
    form_class = MachinesOrderOperationsForm3
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        messages.success(self.request, " تم دفع ضرائب البضاعة بنجاح ", extra_tags="success")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_absolute_url(self):
        messages.success(self.request, "لم يتم دفع ضرائب البضاعة .. لايوجد مال كافي داخل الخزنة ", extra_tags="danger")
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ' دفع ضرائب البضاعة '
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderOperationsCreateTax',
                                             kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(MachinesOrderOperationsCreateTax, self).get_form(*args, **kwargs)
        form.fields['operation_value'].initial = 1.0
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        treasury_balance = form.cleaned_data.get("treasury_name").balance
        operation_value = form.cleaned_data.get("operation_value")
        if float(treasury_balance) >= float(operation_value):
            myform = MachinesOrderOperations()
            myform.order_number = order_number
            myform.operation_type = 5
            myform.operation_value = form.cleaned_data.get("operation_value")
            myform.treasury_name = form.cleaned_data.get("treasury_name")
            myform.operation_date = form.cleaned_data.get("operation_date")
            myform.save()

            treasury = WorkTreasury.objects.get(id=int(form.cleaned_data.get("treasury_name").id))
            treasury.balance -= form.cleaned_data.get("operation_value")
            treasury.save(update_fields=['balance'])

            trans = WorkTreasuryTransactions()
            trans.transaction = 'دفع مبلغ ضرائب بضاعة طلبية رقم ' + str(self.kwargs['pk'])
            trans.treasury = form.cleaned_data.get("treasury_name")
            trans.transaction_type = 1
            trans.value = form.cleaned_data.get("operation_value")
            trans.save()
            
            # to delete notification for machine order operation
            notification = MachineNotifecation.objects.get(machine_order=order_number, notifeaction_type=4)
            notification.delete()
            print("delete_done")
        

            return redirect(self.get_success_url())
        else:
            return redirect(self.get_absolute_url())


class MachinesOrderOperationsCreateOrder(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = MachinesOrderOperations
    form_class = MachinesOrderOperationsForm2
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Machines:MachinesOrdersDetail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استلام البضاعة'
        context['message'] = 'create'
        context['action_url'] = reverse_lazy('Machines:MachinesOrderOperationsCreateOrder',
                                             kwargs={'pk': self.kwargs['pk']})
        return context

    def get_form(self, *args, **kwargs):
        form = super(MachinesOrderOperationsCreateOrder, self).get_form(*args, **kwargs)
        form.fields['operation_date'].initial = datetime.now().date()
        return form

    def form_valid(self, form):
        messages.success(self.request, " تمت عملية استلام البضاعة بنجاح ", extra_tags="success")
        order_number = get_object_or_404(MachinesOrders, id=self.kwargs['pk'])
        myform = MachinesOrderOperations()
        myform.order_number = order_number
        myform.operation_type = 4
        myform.warehouse_name = form.cleaned_data.get("warehouse_name")
        myform.operation_date = form.cleaned_data.get("operation_date")
        myform.save()
        
        # to delete notification for machine order operation
        notification = MachineNotifecation.objects.get(machine_order=order_number, notifeaction_type=3)
        notification.delete()
        print("delete_done")
        
        
        

        op_4 = MachinesOrderOperations.objects.get(order_number=order_number, operation_type=4)
        op_4_date = op_4.operation_date
        op_5_date = op_4_date + timedelta(days=25)
        
        notification2 = MachineNotifecation()  
        notification2.created_at = op_5_date  
        notification2.machine_order = order_number
        notification2.notifeaction_type = 4
        notification2.message = "تنبية بشأن...موعد دفع ضرائب طلب مكينات رقم : " + str(order_number)
        notification2.save()        

        
        
        order_products = MachinesOrderProducts.objects.filter(product_order=order_number, deleted=0)
        order_products_quantity = order_products.aggregate(count=Sum('product_quantity')).get('count')
        order_op3 = MachinesOrderOperations.objects.get(order_number=order_number, operation_type=3)
        order_one_product_op3_cost = float(order_op3.operation_value) / float(order_products_quantity)
        for product in order_products:
            purchase_cost = (float(product.product_price) / float(product.product_quantity)) + float(order_one_product_op3_cost)
            transactions_filter = WarehouseTransactions.objects.filter(item=product.product_name, warehouse=form.cleaned_data.get("warehouse_name"), purchase_cost=purchase_cost)
            if transactions_filter:
                transaction = WarehouseTransactions.objects.get(item=product.product_name, warehouse=form.cleaned_data.get("warehouse_name"), purchase_cost=purchase_cost)
                transaction.quantity += product.product_quantity
                transaction.save(update_fields=['quantity'])
            else:
                transaction = WarehouseTransactions()
                transaction.warehouse = form.cleaned_data.get("warehouse_name")
                transaction.item = product.product_name
                transaction.quantity = product.product_quantity
                transaction.purchase_cost = purchase_cost
                transaction.save()

        return redirect(self.get_success_url())


class MachinesWarehouseDetail(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = WarehouseTransactions
    template_name = 'Machines/machineswarehousestransactions_detail.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = WarehouseTransactions.objects.filter(warehouse=self.kwargs['pk']).order_by('item')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'المخزون الخاص بمخزن الماكينات: ' + str(MachinesWarehouses.objects.get(id=int(self.kwargs['pk'])).name)
        context['type'] = 'list'
        context['count'] = WarehouseTransactions.objects.filter(warehouse=self.kwargs['pk']).order_by('warehouse').count()

        return context
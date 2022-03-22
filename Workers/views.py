import datetime
from itertools import count
from django.db.models.aggregates import Sum
from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import get_object_or_404, redirect , render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from django.views.generic import *

from Core.models import SystemInformation
from .models import *
from .forms import *
from django.contrib import messages
import weasyprint
from django.template.loader import render_to_string
from datetime import datetime, timedelta


class WorkerList(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = Worker
    paginate_by = 6
    template_name = 'Worker/worker_list.html'
    
    def get_queryset(self):
        qureyset = self.model.objects.filter(deleted=False).order_by('-id')
        return qureyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'list'
        context['title'] = 'قائمة العمال'
        context['icons'] = '<i class="fas fa-shapes"></i>'
        context['page'] = 'active'
        context['count'] = self.model.objects.filter(deleted=False).count()
        return context


class WorkerTrachList(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Worker
    paginate_by = 6
    template_name = 'Worker/worker_list.html'
    
    def get_queryset(self):
        queyset = self.model.objects.filter(deleted=True).order_by('-id')
        return queyset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'trach'
        context['count'] = self.model.objects.filter(deleted=True).count()
        return context


class WorkerCreate(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerForm
    template_name = 'forms/form_template.html'
    success_url = reverse_lazy('Workers:workerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'اضافة عامل جديد'
        context['message'] = 'add'
        context['action_url'] = reverse_lazy('Workers:WorkerCreate')
        return context
    
    def get_success_url(self):
        messages.success(self.request, "تم اضافة عامل جديد", extra_tags="success")

        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url
        

class WorkerUpdate(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerForm
    template_name = 'forms/form_template.html'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل عامل: ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerUpdate', kwargs={'pk': self.object.id})
        return context
    
    def get_success_url(self):
        messages.success(self.request,  "تم تعديل العامل " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url        
        

class WorkerDelete(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('Workers:WorkerList')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'نقل العامل الي سلة المهملات: ' + str(self.object)
        context['message'] = 'delete'
        context['action_url'] = reverse_lazy('Workers:WorkerDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم نقل العامل " + str(self.object) + ' الي سلة المهملات بنجاح ' , extra_tags="success")
        myform = Worker.objects.get(id=self.kwargs['pk'])
        myform.deleted = 1
        myform.save()
        return redirect(self.get_success_url())
    
class WorkerRestore(LoginRequiredMixin ,UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'
    

    def get_success_url(self):
        return reverse('Workers:WorkerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'استرجاع العامل: ' + str(self.object)
        context['message'] = 'restore'
        context['action_url'] = reverse_lazy('Workers:WorkerRestore', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم العامل " + str(self.object) + ' الي القائمة بنجاح ' , extra_tags="success")
        myform = Worker.objects.get(id=self.kwargs['pk'])
        myform.deleted = 0
        myform.save()
        return redirect(self.get_success_url())


class WorkerSuperDelete(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = Worker
    form_class = WorkerDeleteForm
    template_name = 'forms/form_template.html'

    def get_success_url(self):
        return reverse('Workers:WorkerTrachList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'حذف العامل : ' + str(self.object)
        context['message'] = 'super_delete'
        context['action_url'] = reverse_lazy('Workers:WorkerSuperDelete', kwargs={'pk': self.object.id})
        return context

    def form_valid(self, form):
        messages.success(self.request, " تم حذف العامل " + str(self.object) + " نهائيا بنجاح ", extra_tags="success")
        my_form = Worker.objects.get(id=self.kwargs['pk'])
        my_form.delete()
        return redirect(self.get_success_url())                      



class WorkerPayments(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_payment.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerPayment.objects.filter(worker=self.object)
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['title'] = 'مسحوبات العامل: ' + str(self.object)
        context['form'] = WorkerPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        return context
    
    
class WorkerPayment_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_payment_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerPayment.objects.filter(worker=self.object).order_by('-id')
        payment_sum = queryset.aggregate(price=Sum('price')).get('price')
        
        
        context = super().get_context_data(**kwargs)
        context['payment'] = queryset.order_by('-id')
        context['payment_sum'] = payment_sum
        context['title'] = 'مسحوبات العامل: ' + str(self.object)
        context['form'] = WorkerPaymentForm(self.request.POST or None)
        context['type'] = 'list'
        return context


class WorkerPaymentUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/auth/login/'
    model = WorkerPayment
    form_class = WorkerPaymentForm
    template_name = 'forms/form_template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'تعديل  مسحوبات يوم : ' + str(self.object)
        context['message'] = 'update'
        context['action_url'] = reverse_lazy('Workers:WorkerPaymentUpdate', kwargs={'pk': self.object.id})
        return context 
    
    def get_success_url(self):
        messages.success(self.request, " تم تعديل المسحوبات " + str(self.object) + " بنجاح ", extra_tags="success")
        if self.request.POST.get('url'):
            return self.request.POST.get('url')
        else:
            return self.success_url

         

def WorkerPaymentCreate(request):
    if request.is_ajax():
        worker_id = request.POST.get('id')
        worker = Worker.objects.get(id=worker_id)
        
        date = request.POST.get('date')
        admin = request.POST.get('admin')
        user = User.objects.get(id=admin)
        price = request.POST.get('price')
        
        if worker_id and date and admin and price:
            obj = WorkerPayment()
            obj.worker = worker
            obj.date = date
            obj.admin = user
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

    
def WorkerPaymentDelete(request):
    if request.is_ajax():
        payment_id = request.POST.get('payment_id')
        obj =  WorkerPayment.objects.get(id=payment_id)
        obj.delete()
        
        if obj:
            response = {
                'msg' : 'Send Successfully'
            }

        return JsonResponse(response)


class WorkerPaymentReport(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    model = WorkerPayment
    form = WorkerPaymentReportForm()
    template_name = 'Worker_Reports/worker_payment_report.html'
    
   
    def queryset(self):
        if not self.request.GET.get('submit'):
            queryset = None
        else:
            queryset = WorkerPayment.objects.filter(worker = self.kwargs['pk']).order_by('-id')
            if self.request.GET.get('from_date'):
                queryset = queryset.filter(date__gte = self.request.GET.get('from_date'))
            if self.request.GET.get('to_date'):
                queryset = queryset.filter(date__lte = self.request.GET.get('to_date'))
                                  
        return queryset 
    
    def get_sum_price(self):
        queryset = self.queryset()
        if queryset != None:
            sum_price =  queryset.aggregate(price=Sum('price')).get('price')
        else:
            sum_price = 0
        total = {
            'sum_price' :sum_price
        }
        return total
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['summary'] = self.get_sum_price()
        context['name'] = Worker.objects.get(id=self.kwargs['pk'])
        return context
    

def PrintWorkerPayment(request,pk):
    worker = Worker.objects.get(id=pk)
    system_info = SystemInformation.objects.all()
    if system_info.count() > 0:
        system_info = system_info.last()
    else:
        system_info = None
            
    queryset = WorkerPayment.objects.filter(worker=pk).order_by('-id')
    if request.GET.get('from_date'):
        queryset = queryset.filter(date__gte = request.GET.get('from_date'))
    if request.GET.get('to_date'):
        queryset = queryset.filter(date__lte = request.GET.get('to_date'))
    
   
    context = {
        'queryset':queryset,
        'count_price':  queryset.aggregate(price=Sum('price')).get('price'),
        'system_info':system_info,
        'date': datetime.now(),
        'user': request.user.username,
        'from_date': request.GET.get('from_date'),
        'to_date': request.GET.get('to_date'),
        'worker':worker,
    }
    html_string = render_to_string('Worker_Reports/print_worker_payment.html', context)
    html = weasyprint.HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf = html.write_pdf(stylesheets=[weasyprint.CSS('static/assets/css/invoice_pdf.css')], presentational_hints=True)
    response = HttpResponse(pdf, content_type='application/pdf')
    return response    



class WorkerAttendances(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_attendance.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerAttendance.objects.filter(worker=self.object)
        days_count = queryset.count()
        context = super().get_context_data(**kwargs)
        context['worker'] = queryset.order_by('-id')
        context['days_count'] = days_count
        context['title'] = 'حضور العامل: ' + str(self.object)
        context['form'] = WorkerAttendanceForm(self.request.POST or None)
        context['type'] = 'list'
        return context
    
    
class WorkerAttendance_div(LoginRequiredMixin, DetailView):
    login_url = '/auth/login/'
    model = Worker
    template_name = 'Worker/worker_attendance_div.html'
    
    def get_context_data(self, **kwargs):
        queryset = WorkerAttendance.objects.filter(worker=self.object)
        days_count = queryset.count()
        context = super().get_context_data(**kwargs)
        context['worker'] = queryset.order_by('-id')
        context['days_count'] = days_count
        context['title'] = 'حضور العامل : ' + str(self.object)
        context['form'] = WorkerAttendanceForm(self.request.POST or None)
        context['type'] = 'list'
        return context


def WorkerAttendanceCreate(request):
    if request.is_ajax():
        worker_id = request.POST.get('id')
        
        worker = Worker.objects.get(id=worker_id)
        print(worker)
        
        date = request.POST.get('date')
        print(date)
        hour_count = request.POST.get('hour_count')
        print(hour_count)
        user = request.user
        print(user)
        
        
        if  date and hour_count:
            obj = WorkerAttendance()
            obj.worker = worker
            obj.date = date
            obj.hour_count = hour_count
            obj.attend = True
            obj.admin = user
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
    
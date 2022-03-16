from django.contrib import admin

from Workers.models import Worker, WorkerPayment

# Register your models here.
admin.site.register(Worker)
admin.site.register(WorkerPayment)
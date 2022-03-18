
from django.urls import path
from .views import * 

app_name = 'Factories'
urlpatterns = [
    path('list/', FactoryList.as_view(), name="FactoryList"),
    path('trach/', FactoryTrachList.as_view(), name="FactoryTrachList"),
    path('create/', FactoryCreate.as_view(), name="FactoryCreate"),
    path('update/<int:pk>', FactoryUpdate.as_view(), name="FactoryUpdate"),
    path('delete/<int:pk>', FactoryDelete.as_view(), name="FactoryDelete"),
    path('restore/<int:pk>', FactoryRestore.as_view(), name="FactoryRestore"),
    path('superDelete/<int:pk>', FactorySuperDelete.as_view(), name="FactorySuperDelete"),
    path('detail/payment/<int:pk>', FactoryPayment.as_view(), name="FactoryPayment"),
    path('detail/payment/<int:pk>/div/', FactoryPayment_div.as_view(), name="FactoryPayment_div"),
    
    path('payment/create/', FactoryPaymentCreate, name="FactoryPaymentCreate"),
    path('payment/delete/', FactoryPaymentDelete, name="FactoryPaymentDelete"),
    path('payment/update/<int:pk>/', FactoryPaymentUpdate.as_view(), name="FactoryPaymentUpdate"),
    path('payment/report/<int:pk>/', FactoryPaymentReport.as_view(), name="FactoryPaymentReport"),
    path('payment/print/<int:pk>/', PrintPayment , name="PrintPayment"),
    
    
    path('outside/<int:pk>', FactoryOutside.as_view(), name="FactoryOutside"),
    path('outside/<int:pk>/div/', FactoryOutSide_div.as_view(), name="FactoryOutSide_div"),
    path('outside/<int:pk>/update/', FactoryOutSideUpdate.as_view(), name="FactoryOutSideUpdate"),
    path('outside/report/<int:pk>/', FactoryOutSideReport.as_view(), name="FactoryOutSideReport"),
    path('outside/create/', FactoryOutSideCreate, name="FactoryOutSideCreate"),# url for create function using ajax
    path('outside/delete/', FactoryOutsideDelete, name="FactoryOutsideDelete"), # url for delete function using ajax
    path('outside/print/<int:pk>/', PrintOutside , name="PrintOutside"),
    
    path('inside/<int:pk>', FactoryInside.as_view(), name="FactoryInside"),
    path('inside/<int:pk>/div/', FactoryInSide_div.as_view(), name="FactoryInSide_div"),
    path('inside/<int:pk>/update/', FactoryInSideUpdate.as_view(), name="FactoryInSideUpdate"), 
    path('inside/create/', FactoryInSideCreate, name="FactoryInSideCreate"),# url for create function using ajax
    path('inside/delete/', FactoryInsideDelete, name="FactoryInsideDelete"), # url for delete function using ajax
    path('inside/report/<int:pk>/', FactoryInSideReport.as_view(), name="FactoryInSideReport"),
    path('inside/print/<int:pk>/', PrintInside , name="PrintInside"),
    
    
]

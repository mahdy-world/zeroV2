from django.urls import path 
from . import views

app_name = 'Core'
urlpatterns = [
    path('', views.Index, name='index'),
    path('systemInfoCreate/', views.SystemInfoCreate.as_view(), name='SystemInfoCreate'),
    path('systemInfoUpdate/<int:pk>/', views.SystemInfoUpdate.as_view(), name='SystemInfoUpdate'),
    path('MachineSearch/', views.MachineSearch.as_view(), name='MachineSearch'),
    path('SparePartsSearch/', views.SparePartsSearch.as_view(), name='SparePartsSearch'),
    path('SparePartsOrderSearch/', views.SparePartsOrderSearch.as_view(), name='SparePartsOrderSearch'),
    path('MachineOrderSearch/', views.MachineOrderSearch.as_view(), name='MachineOrderSearch'),
    path('factory_search/', views.FactorySearch.as_view(), name='FactorySearch'),
    path('product_search/', views.ProductSearch.as_view(), name='ProductSearch'),
    path('seller_search/', views.SellerSearch.as_view(), name='SellerSearch'),
    path('worker_search/', views.WorkerSearch.as_view(), name='WorkerSearch'),

    
    path('read/', views.Read, name='Read'),
    
]

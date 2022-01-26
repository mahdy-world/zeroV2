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
    
    
    path('read/', views.Read, name='Read'),
    
]

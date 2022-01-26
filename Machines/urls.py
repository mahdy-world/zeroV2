from django.urls import path 
from .views import *

app_name = 'Machines'
urlpatterns = [
    path('types_active_list/', TypesActiveList.as_view(), name='types_active_list'),
    path('types_trash_list/', TypesTrashList.as_view(), name='types_trash_list'),
    path('types_create/', TypesCreate.as_view(), name='types_create'),
    path('types_update/<int:pk>/edit/', TypesUpdate.as_view(), name='types_update'),
    path('types_delete/<int:pk>/edit/', TypesDelete.as_view(), name='types_delete'),
    path('types_restore/<int:pk>/restore/', TypesRestore.as_view(), name='types_restore'),
    path('types_super_delete/<int:pk>/super_delete/', TypesSuperDelete.as_view(), name='types_super_delete'),
    ###############################################################################
    
    
    
    path('warehouses_active_list/', WarehousesActiveList.as_view(), name='warehouses_active_list'),
    path('warehouses_trash_list/', WarehousesTrashList.as_view(), name='warehouses_trash_list'),
    path('warehouses_create/', WarehousesCreate.as_view(), name='warehouses_create'),
    path('warehouses_update/<int:pk>/edit/', WarehousesUpdate.as_view(), name='warehouses_update'),
    path('warehouses_delete/<int:pk>/edit/', WarehousesDelete.as_view(), name='warehouses_delete'),
    path('warehouses_restore/<int:pk>/restore/', WarehousesRestore.as_view(), name='warehouses_restore'),
    path('warehouses_super_delete/<int:pk>/super_delete/', WarehousesSuperDelete.as_view(), name='warehouses_super_delete'),
    path('warehouses_detail/<int:pk>/detail/', MachinesWarehouseDetail.as_view(), name='warehouses_detail'),
    ###############################################################################
    
    
    path('names_active_list/', NamesActiveList.as_view(), name='names_active_list'),
    path('names_trash_list/', NamesTrashList.as_view(), name='names_trash_list'),
    path('names_create/', NamesCreate.as_view(), name='names_create'),
    path('names_update/<int:pk>/edit/', NamesUpdate.as_view(), name='names_update'),
    path('names_delete/<int:pk>/edit/', NamesDelete.as_view(), name='names_delete'),
    path('names_restore/<int:pk>/restore/', NamesRestore.as_view(), name='names_restore'),
    path('names_detail/<int:pk>/<str:name>/detail/', NamesDetail.as_view(), name='NamesDetail'),
    path('names_super_delete/<int:pk>/super_delete/', NamesSuperDelete.as_view(), name='names_super_delete'),
    ###############################################################################
    
    
    path('suppliers_active_list/', SuppliersActiveList.as_view(), name='suppliers_active_list'),
    path('suppliers_trash_list/', SuppliersTrashList.as_view(), name='suppliers_trash_list'),
    path('suppliers_create/', SuppliersCreate.as_view(), name='suppliers_create'),
    path('suppliers_update/<int:pk>/edit/', SuppliersUpdate.as_view(), name='suppliers_update'),
    path('suppliers_delete/<int:pk>/edit/', SuppliersDelete.as_view(), name='suppliers_delete'),
    path('suppliers_restore/<int:pk>/restore/', SuppliersRestore.as_view(), name='suppliers_restore'),
    path('suppliers_super_delete/<int:pk>/super_delete/', SuppliersSuperDelete.as_view(), name='suppliers_super_delete'),
    ###############################################################################
    ###############################################################################
    
    
    path('MachinesOrdersList/', MachinesOrdersList.as_view(), name="MachinesOrdersList"),
    path('MachinesOrdersTrashList/', MachinesOrdersTrashList.as_view(), name="MachinesOrdersTrashList"),
    path('MachinesOrdersCreate/create/', MachinesOrdersCreate.as_view(), name='MachinesOrdersCreate'),
    path('MachinesOrdersDetail/<int:pk>/detail/', MachinesOrdersDetail, name='MachinesOrdersDetail'),
    path('MachinesOrdersUpdate/<int:pk>/update/', MachinesOrdersUpdate.as_view(), name='MachinesOrdersUpdate'),
    path('MachinesOrdersDelete/<int:pk>/delete/', MachinesOrdersDelete.as_view(), name='MachinesOrdersDelete'),
    path('MachinesOrdersRestore/<int:pk>/restore/', MachinesOrdersRestore.as_view(), name='MachinesOrdersRestore'),
    path('MachinesOrdersSuperDelete/<int:pk>/super_delete/', MachinesOrdersSuperDelete.as_view(), name='MachinesOrdersSuperDelete'),
    ###############################################################################
    
    
    path('AddProductOrder/<int:pk>/create/', AddProductOrder, name='AddProductOrder'),
    path('MachinesOrderProductsUpdate/<int:pk>/<int:id>/update/', MachinesOrderProductsUpdate.as_view(), name='MachinesOrderProductsUpdate'),
    path('MachinesOrderProductsDelete/<int:pk>/<int:id>/Delete/', MachinesOrderProductsDelete.as_view(), name='MachinesOrderProductsDelete'),
    ###############################################################################
    
    
    path('MachinesOrderOperationsCreateDeposit/<int:pk>/create_deposite/', MachinesOrderOperationsCreateDeposit.as_view(), name='MachinesOrderOperationsCreateDeposit'),
    path('MachinesOrderOperationsCreateReset/<int:pk>/create_reset/', MachinesOrderOperationsCreateReset.as_view(), name='MachinesOrderOperationsCreateReset'),
    path('MachinesOrderOperationsCreateClearance/<int:pk>/create_clearance/', MachinesOrderOperationsCreateClearance.as_view(), name='MachinesOrderOperationsCreateClearance'),
    path('MachinesOrderOperationsCreateOrder/<int:pk>/create_order/', MachinesOrderOperationsCreateOrder.as_view(), name='MachinesOrderOperationsCreateOrder'),
    path('MachinesOrderOperationsCreateTax/<int:pk>/create_tax/', MachinesOrderOperationsCreateTax.as_view(), name='MachinesOrderOperationsCreateTax'),
]

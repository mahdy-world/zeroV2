from django.urls import path 
from .views import *

app_name = 'SpareParts'
urlpatterns = [
   # Spare Parts Type Module 
   path('sparepartsList/', SparePartsTypeList.as_view(), name="SpareTypeList" ),
   path('sparepartsTrachList/', SparePartsTypeTrachList.as_view(), name="SpareTypeTrachList" ),
   path('sparepartsType/create/', SparePartsTypeCreate.as_view(), name='SparePartsTypeCreate'),
   path('sparepartsType/<int:pk>/update/', SparePartsTypeUpdate.as_view(), name='SparePartsTypeUpdate'),
   path('sparepartsType/<int:pk>/delete/', SparePartsTypeDelete.as_view(), name='SparePartsTypeDelete'),
   path('sparepartsType/<int:pk>/restore/', SparePartsTypeRestore.as_view(), name='SparePartsTypeRestore'),
   path('sparepartsType/<int:pk>/super_delete/', SparePartsTypeSuperDelete.as_view(), name='SparePartsTypeSuperDelete'),
   #-------------------------------------------------------------------------------------------------------
   
   # Spare Parts Names Module 
   path('sparepartsNameList/', SparePartsNameList.as_view(), name="SparePartsNameList" ),
   path('sparepartsNameTrachList/', SparePartsNameTrachList.as_view(), name="SpareNameTrachList" ),
   path('sparepartsName/create/', SparePartsNameCreate.as_view(), name='SparePartsNameCreate'),
   path('sparepartsName/<int:pk>/update/', SparePartsNameUpdate.as_view(), name='SparePartsNameUpdate'),
   path('sparepartsWarehouse/<int:pk>/<str:name>/detail/', SparePartsNamesDetail.as_view(), name='SparePartsNamesDetail'),
   path('sparepartsName/<int:pk>/delete/', SparePartsNameDelete.as_view(), name='SparePartsNameDelete'),
   path('sparepartsName/<int:pk>/restore/', SparePartsNameRestore.as_view(), name='SparePartsNameRestore'),
   path('sparepartsName/<int:pk>/super_delete/', SparePartsNameSuperDelete.as_view(), name='SparePartsNameSuperDelete'),
   #-------------------------------------------------------------------------------------------------------
   
   
   # Spare Parts Warehouses Module 
   path('sparepartsWarehouseList/', SparePartsWarehouseList.as_view(), name="SparePartsWarehouseList" ),
   path('sparepartsWarehouseTrachList/', SparePartsWarehouseTrachList.as_view(), name="SparePartsWarehouseTrachList" ),
   path('sparepartsWarehouse/create/', SparePartsWarehouseCreate.as_view(), name='SparePartsWarehouseCreate'),
   path('sparepartsWarehouse/<int:pk>/update/', SparePartsWarehouseUpdate.as_view(), name='SparePartsWarehouseUpdate'),
   path('sparepartsWarehouse/<int:pk>/delete/', SparePartsWarehouseDelete.as_view(), name='SparePartsWarehouseDelete'),
   path('sparepartsWarehouse/<int:pk>/restore/', SparePartsWarehouseRestore.as_view(), name='SparePartsWarehouseRestore'),
   path('sparepartsWarehouse/<int:pk>/super_delete/', SparePartsWarehouseSuperDelete.as_view(), name='SparePartsWarehouseSuperDelete'),
   path('sparepartsWarehouse/<int:pk>/detail/', SparePartsWarehouseDetail.as_view(), name='SparePartsWarehouseDetail'),
   #-------------------------------------------------------------------------------------------------------
   
   
   # Spare Parts Supplier Module 
   path('sparepartsSupplierList/', SparePartsSupplierList.as_view(), name="SparePartsSupplierList" ),
   path('sparepartsSupplierTrachList/', SparePartsSupplierTrachList.as_view(), name="SparePartsSupplierTrachList" ),
   path('sparepartsSupplier/create/', SparePartsSupplierCreate.as_view(), name='SparePartsSupplierCreate'),
   path('sparepartsSupplier/<int:pk>/update/', SparePartsSupplierUpdate.as_view(), name='SparePartsSupplierUpdate'),
   path('sparepartsSupplier/<int:pk>/delete/', SparePartsSupplierDelete.as_view(), name='SparePartsSupplierDelete'),
   path('sparepartsSupplier/<int:pk>/restore/', SparePartsSupplierRestore.as_view(), name='SparePartsSupplierRestore'),
   path('sparepartsSupplier/<int:pk>/super_delete/', SparePartsSupplierSuperDelete.as_view(), name='SparePartsSupplierSuperDelete'),
   #--------------------------------------------------------------------------------------------------------------------
   
   # Spare Parts Orders Module 
   path('sparepartsOrdersList/', SparePartsOrderList.as_view(), name="SparePartsOrderList" ),
   path('sparepartsOrderTrachList/', SparePartsOrderTrachList.as_view(), name="SparePartsOrderTrachList" ),
   path('sparepartsOrder/create/', SparePartsOrderCreate.as_view(), name='SparePartsOrderCreate'),
   path('sparepartsOrder/<int:pk>/detail/', SparePartsOrderDetail, name='SparePartsOrderDetail'),
   path('sparepartsOrder/<int:pk>/update/', SparePartsOrderUpdate.as_view(), name='SparePartsOrderUpdate'),
   path('sparepartsOrder/<int:pk>/delete/', SparePartsOrderDelete.as_view(), name='SparePartsOrderDelete'),
   path('sparepartsOrder/<int:pk>/restore/', SparePartsOrderRestore.as_view(), name='SparePartsOrderRestore'),
   path('sparepartsOrder/<int:pk>/super_delete/', SparePartsOrderSuperDelete.as_view(), name='SparePartsOrderSuperDelete'),
   path('sparepartsOrderProduct/<int:pk>/create/', AddProductOrder, name='AddProductOrder'),
   path('sparepartsOrderProduct/<int:pk>/<int:id>/update/', SparePartsOrderAddProductUpdate.as_view(), name='SparePartsOrderAddProductUpdate'),
   path('sparepartsOrderProduct/<int:pk>/<int:id>/Delete/', SparePartsOrderAddProductDelete.as_view(), name='SparePartsOrderAddProductDelete'),
   
   # Operations
   path('sparepartsOrderOperation/<int:pk>/create_deposite/', SparePartsOperationCreateDeposit.as_view(), name='SparePartsOperationCreateDeposit'),
   path('sparepartsOrderOperation/<int:pk>/create_reset/', SparePartsOperationCreateReset.as_view(), name='SparePartsOperationCreateReset'),
   path('sparepartsOrderOperation/<int:pk>/create_clearance/', SparePartsOperationCreateClearance.as_view(), name='SparePartsOperationCreateClearance'),
   path('sparepartsOrderOperation/<int:pk>/create_order/', SparePartsOperationCreateOrder.as_view(), name='SparePartsOperationCreateOrder'),
   path('sparepartsOrderOperation/<int:pk>/create_tax/', SparePartsOperationCreateTax.as_view(), name='SparePartsOperationCreateTax'),

]

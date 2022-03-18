from django.urls import path
from .views import * 

app_name = 'Products'
urlpatterns = [
    path('list/', ProductList.as_view(), name="ProductList"),
    path('trach/', ProductTrachList.as_view(), name="ProductTrachList"),
    path('create/', ProductCreate.as_view(), name="ProductCreate"),
    path('update/<int:pk>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('add_quantity/<int:pk>', AddProductQuantity.as_view(), name="AddProductQuantity"),
    path('delete/<int:pk>', ProductDelete.as_view(), name="ProductDelete"),
    path('restore/<int:pk>', ProductRestore.as_view(), name="ProductRestore"),
    path('superDelete/<int:pk>', ProductSuperDelete.as_view(), name="ProductSuperDelete"),
    ######################################################################################
    path('seller_list/', SellerList.as_view(), name="SellerList"),
    path('seller_trash/', SellerTrashList.as_view(), name="SellerTrashList"),
    path('seller_create/', SellerCreate.as_view(), name="SellerCreate"),
    path('seller_update/<int:pk>', SellerUpdate.as_view(), name="SellerUpdate"),
    path('seller_paid_value/<int:pk>', PaidSellerValue.as_view(), name="PaidSellerValue"),
    path('seller_delete/<int:pk>', SellerDelete.as_view(), name="SellerDelete"),
    path('seller_restore/<int:pk>', SellerRestore.as_view(), name="SellerRestore"),
    path('seller_superDelete/<int:pk>', SellerSuperDelete.as_view(), name="SellerSuperDelete"),
]

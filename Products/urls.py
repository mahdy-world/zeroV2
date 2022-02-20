from django.urls import path
from .views import * 

app_name = 'Products'
urlpatterns = [
    path('list/', ProductList.as_view(), name="ProductList"),
    path('trach/', ProductTrachList.as_view(), name="ProductTrachList"),
    path('create/', ProductCreate.as_view(), name="ProductCreate"),
    path('update/<int:pk>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('delete/<int:pk>', ProductDelete.as_view(), name="ProductDelete"),
    path('restore/<int:pk>', ProductRestore.as_view(), name="ProductRestore"),
    path('superDelete/<int:pk>', ProductSuperDelete.as_view(), name="ProductSuperDelete"),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('d-product-list/', product_list, name='d-product-list'),
    path('category-list', category_list, name='category-list'),
    path('edit/<int:pk>/', edit_p, name='edit'),
    path('company', company_list, name='company'),
    path('company-detail/<int:company_id>/', company_detail, name='company-detail'),
    path('d-order-list', order_list, name='d-order-list'),
    path('add-product', add_product, name='add-product'),
    path('edit-status/<int:pk>/', edit_status, name='edit-status'),
    path('submit_an_ad/', submit_an_ad, name='submit_an_ad'),
]
from django.urls import path
from .views import *


urlpatterns = [
    path('', product_list, name='product-list'),
    path('catalog/<int:pk>/', product_detail, name='product-detail'),
    path('company/<int:pk>/', company_products, name='company-products'),
    path('catalog/<slug:slug>/', category_catalog, name='category-catalog'),
    path('cart-page', cart_page, name="cart-page"),
    path('shipping-adress/', shipping_page, name='shipping-page'),  
    path('favorites-page', favorites_page, name='favorites-page'),
    path('pending', pending_page, name='pending') ,
    path('purchases', purchases, name='purchases'),
    path('process-order/', process_order, name='process-order'),
    path('become-seller', become_seller_page, name='become-seller')

]
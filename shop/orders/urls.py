from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('', Basket.as_view(), name='orders_index'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('add_order/', OrderCreate.as_view(), name='order_add'),
    # path('order_created/', order_created, name='order_created'),
    path('payment<int:pk>/', create_payment, name='payment'),
]

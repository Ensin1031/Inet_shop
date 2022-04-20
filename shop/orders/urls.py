from django.urls import path

from .views import *

app_name = 'orders'

urlpatterns = [
    path('', cart_detail, name='orders_index'),
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]

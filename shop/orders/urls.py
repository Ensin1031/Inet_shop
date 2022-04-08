from django.urls import path

from .views import *


urlpatterns = [
    path('', orders_index, name='orders_index'),
]

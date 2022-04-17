from django.urls import path

from .views import *


urlpatterns = [
    path('<str:slug>/', OrderGood.as_view(), name='orders_index'),
]

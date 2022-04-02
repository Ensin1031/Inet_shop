from django.urls import path

from .views import *

urlpatterns = [
    path('', shopping, name='shopping'),
]

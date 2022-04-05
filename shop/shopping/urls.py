from django.urls import path

from .views import *


urlpatterns = [
    path('', shopping, name='shopping'),
    path('products/', category, name='products'),
    path('category/<str:slug>/', get_category, name='category'),
    path('show_image/<str:slug>/', show_image, name='show_image'),
    path('brand/<str:slug>/', get_brand, name='brand'),
    path('good/<str:slug>/', show_good, name='good'),
]

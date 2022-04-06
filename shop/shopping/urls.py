from django.urls import path

from .views import *


urlpatterns = [
    path('', ShowAllGoods.as_view(), name='shopping'),
    path('category/<str:slug>/', get_category, name='category'),
    path('show_image/<str:slug>/', show_image, name='show_image'),
    path('brand/<str:slug>/', get_brand, name='brand'),
    path('good/<str:slug>/', ShowGood.as_view(), name='good'),
]

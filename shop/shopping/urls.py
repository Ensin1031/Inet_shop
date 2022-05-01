from django.urls import path

from .views import *


urlpatterns = [
    path('', ShowAllGoods.as_view(), name='shopping'),
    path('good/<str:slug>/', ShowGood.as_view(), name='good'),
    path('category/<str:slug_cat>/', ShowAllGoods.as_view(), name='category'),
    path('brand/<str:slug_brand>/', ShowAllGoods.as_view(), name='brand'),
    path('search/', shopping_search, name='pre_search'),
    path('search_"<str:search_result>"/', ShowAllGoods.as_view(), name='search_result'),
    # path('show_image/<str:slug>/', show_image, name='show_image'),
]

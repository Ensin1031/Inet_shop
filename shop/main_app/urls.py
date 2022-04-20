from django.urls import path, include
from django.contrib.flatpages import views
from .views import *


urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('search/', SearchGoodView.as_view(), name='search'),
    path('about/', views.flatpage, {'url': '/about/'}, name='about'),
    path('contact/', views.flatpage, {'url': '/contact/'}, name='contact'),
    path('payments/', views.flatpage, {'url': '/payments/'}, name='payments'),
    path('delivery/', views.flatpage, {'url': '/delivery/'}, name='delivery'),
    path('faqs/', views.flatpage, {'url': '/faqs/'}, name='faqs'),
    path('support/', views.flatpage, {'url': '/support/'}, name='support'),
    path('privacy/', views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('warranty/', views.flatpage, {'url': '/warranty/'}, name='warranty'),
    path('conditions/', views.flatpage, {'url': '/conditions/'}, name='conditions'),
    path('return/', views.flatpage, {'url': '/return/'}, name='return'),
    path('intellproperty/', views.flatpage, {'url': '/intellproperty/'}, name='intellproperty'),
    path('promo/<str:slug_promo>/', PromotionView.as_view(), name='promo'),
]
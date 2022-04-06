from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('search/', SearchGoodView.as_view(), name='search'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('faqs/', FAQsView.as_view(), name='faqs'),
    path('support/', SupportView.as_view(), name='support'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('warranty/', WarrantyView.as_view(), name='warranty'),
    path('conditions/', ConditionsView.as_view(), name='conditions'),
    path('return/', ReturnView.as_view(), name='return'),
    path('intellproperty/', IntellPropertyView.as_view(), name='intellproperty'),
]

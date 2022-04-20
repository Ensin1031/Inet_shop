from django.http import request
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from shop.settings import LOGIN_REDIRECT_URL
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=LOGIN_REDIRECT_URL), name='logout'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('my_account/', MyAccountView.as_view(), name='my_account')
]

from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/activate/<str:sign>/', user_activate,
         name='register_activate'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
            template_name='registration/pass_reset_done.html'
    ), name='password_reset_done'),
    path('password_reset/', ShopPasswordResetView.as_view(),
         name='password_reset'),
    path('reset/done/', PasswordResetCompleteView.as_view(
            template_name='registration/pass_reset_complete.html'
    ), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
            template_name='registration/pass_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('my_account/profile/', ChangeUserInfoView.as_view(), name='profile'),
    path('my_account/orders/', OrderUserView.as_view(), name='orders'),
    path('my_account/reviews/', ReviewUserView.as_view(), name='reviews'),
    path('my_account/delete/', DeleteUserView.as_view(), name='delete'),
    path('my_account/', MyAccountView.as_view(), name='my_account'),
]

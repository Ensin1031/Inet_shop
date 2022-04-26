from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from django.contrib.auth.views import PasswordResetView

from .forms import ChangeUserAddressForm, RegisterUserForm, ChangeUserInfoForm
from .models import ShopUser
from .utilities import signer
from shopping.models import ReviewsDB
from orders.models import OrderDB, OrderItemDB


class RegisterUserView(CreateView):
    """"""
    model = ShopUser
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    """"""
    template_name = 'registration/register_done.html'


def user_activate(request, sign):
    """"""
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'registration/bad_signature.html')
    user = get_object_or_404(ShopUser, username=username)
    if user.is_activated:
        template = 'registration/user_is_activated.html'
    else:
        template = 'registration/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class ShopPasswordResetView(PasswordResetView):
    """"""
    template_name = 'registration/pass_reset_form.html'
    subject_template_name = 'email/pass_reset_subject.txt'
    email_template_name = 'email/pass_reset_email.txt'
    success_url = reverse_lazy('password_reset_done')
    extra_email_context = {'domain': 'localhost:8000'}


class MyAccountView(LoginRequiredMixin, ListView):
    """"""
    template_name = 'accounts/account.html'
    model = ShopUser

    def get_queryset(self):
        pass


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """"""
    model = ShopUser
    template_name = 'accounts/profile.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Ваши личные данные изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ChangeUserAddressView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """"""
    model = ShopUser
    template_name = 'accounts/address.html'
    form_class = ChangeUserAddressForm
    success_url = reverse_lazy('address')
    success_message = 'Ваши изменения адреса сохранены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ReviewUserView(LoginRequiredMixin, ListView):
    """"""
    model = ShopUser
    template_name = 'accounts/reviews.html'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = ReviewsDB.objects.filter(user_name__pk=self.user_id).select_related('user_name', 'good')
        return context


class OrderUserView(LoginRequiredMixin, ListView):
    """"""
    model = ShopUser
    template_name = 'accounts/orders.html'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = OrderDB.objects.filter(for_user__pk=self.user_id)
        return context


class DeleteUserView(LoginRequiredMixin, DeleteView):
    """"""
    model = ShopUser
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

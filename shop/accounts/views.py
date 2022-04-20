from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature

from .forms import RegisterUserForm
from .models import ShopUser
from .utilities import signer


# todo forgot password

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


# TODO template, tags?
class MyAccountView(LoginRequiredMixin, ListView):
    """"""
    template_name = 'accounts/account.html'
    model = ShopUser

    def get_queryset(self):
        pass




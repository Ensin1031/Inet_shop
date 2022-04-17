from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView

from .models import *
from shopping.models import GoodsDB


def order_index(request, slug):
    return render(request, 'orders/index.html', {'title': f'Покупка {slug}'})


class OrderGood(LoginRequiredMixin, DetailView):
    """Sale of goods purchased"""
    model = GoodsDB
    template_name = 'orders/index.html'

    def get_context_data(self, **kwargs):
        context = super(OrderGood, self).get_context_data(**kwargs)
        context['title'] = 'Покупка'

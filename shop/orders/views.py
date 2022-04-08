from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView


from .models import *


def orders_index(request):
    '''тестовая функция обработки покупки заказа'''
    return render(request, 'orders/index.html', {'hello': 'Hello, orders!'})


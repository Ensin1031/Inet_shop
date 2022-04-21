from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
# from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .cart import Cart
from .forms import CartAddProductForm
from shopping.models import GoodsDB


@require_POST
def cart_add(request, product_id):
    """обработчик добавления товара в корзину."""
    cart = Cart(request)
    product = get_object_or_404(GoodsDB, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(good=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('orders:orders_index')


def cart_remove(request, product_id):
    """обработчик удаления товаров из корзины"""
    cart = Cart(request)
    product = get_object_or_404(GoodsDB, id=product_id)
    cart.remove(product)
    return redirect('orders:orders_index')


def cart_detail(request):
    """будет отображать корзину, основываясь на данной сессии"""
    cart = Cart(request)
    for item in cart:       # возможность изменять количество товара в корзине
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'orders/basket.html', {'cart': cart})

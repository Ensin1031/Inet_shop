from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import OrderDB, OrderItemDB
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


# def cart_detail(request):
#     """будет отображать корзину, основываясь на данной сессии"""
#     cart = Cart(request)
#     for item in cart:       # возможность изменять количество товара в корзине
#         item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
#                                                                    'update': True})
#     return render(request, 'orders/basket.html', {'cart': cart})


class Basket(TemplateView):
    """будет отображать корзину, основываясь на данной сессии"""
    template_name = 'orders/basket.html'

    def get_context_data(self, **kwargs):
        context = super(Basket, self).get_context_data(**kwargs)
        cart = Cart(self.request)
        for item in cart:
            item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                       'update': True})
        context['cart'] = cart
        context['breadcrumb_list'] = self.request.path[1: -1].split('/')
        return context


class OrderCreate(LoginRequiredMixin, CreateView):
    """Create an order record in the model OrderDB"""
    form_class = OrderCreateForm
    template_name = 'orders/order.html'
    raise_exception = True

    def form_valid(self, form):
        cart = Cart(self.request)
        form.instance.for_user = self.request.user
        order = form.save()
        for item in cart:
            OrderItemDB.objects.create(order=order,
                                       product=item['product'],
                                       price=item['price'],
                                       quantity=item['quantity'])
            views = item['product']         # накручиваем просмотры
            views.n_views = F('n_views') + 1
            views.save()

        cart.clear()
        return super(OrderCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['breadcrumb_list'] = self.request.path[1: -1].split('/')
        return context


def create_payment(request, pk):
    print(request, pk)
    return render(request, 'orders/pay.html', {'order': pk})

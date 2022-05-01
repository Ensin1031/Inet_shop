from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, CreateView, \
    TemplateView

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import OrderDB, OrderItemDB
from shopping.models import GoodsDB
from .tasks import send_admin_mail


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
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    else:
        return redirect('orders:orders_index')


def cart_remove(request, product_id):
    """обработчик удаления товаров из корзины"""
    cart = Cart(request)
    product = get_object_or_404(GoodsDB, id=product_id)
    cart.remove(product)
    return redirect('orders:orders_index')


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
        return context


class OrderCreate(LoginRequiredMixin, CreateView):
    """Create an order record in the model OrderDB"""
    form_class = OrderCreateForm
    template_name = 'orders/order.html'
    raise_exception = True

    def form_valid(self, form):
        cart = Cart(self.request)
        if len(cart) > 0:
            form.instance.for_user = self.request.user
            order = form.save()
            send_admin_mail.delay(order.id)
            for item in cart:
                OrderItemDB.objects.create(order=order,
                                           product=item['product'],
                                           price=item['price'],
                                           quantity=item['quantity'])
                views = item['product']             # накручиваем просмотры ))
                views.n_views = F('n_views') + 1
                views.save()

            cart.clear()
            return super(OrderCreate, self).form_valid(form)
        else:
            return super(OrderCreate, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        return context


class OrderCreated(LoginRequiredMixin, DetailView):
    """"""
    model = OrderDB
    template_name = 'orders/order_created.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = OrderItemDB.objects.filter(order__pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        queryset = OrderDB.objects.filter(pk=self.kwargs.get('pk'))
        return queryset


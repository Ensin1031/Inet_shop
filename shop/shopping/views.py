from django.contrib import messages
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import AddReviewForm
from orders.forms import CartAddProductForm
from .get_func import *
from .filters import GoodsFilter
from main_app.models import *


class ShowGood(CreateView, DetailView):
    """Single product page class"""
    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'
    form_class = AddReviewForm

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_name = self.request.user
            form.instance.good = GoodsDB.objects.filter(slug=self.kwargs.get('slug')).first()
            return super(ShowGood, self).form_valid(form)
        else:
            raise Http404('Для отправки своего отзыва Вы должны зарегистрироваться или залогиниться')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.filter(product=context['object'])
        context['reviews'] = ReviewsDB.objects.filter(good=context['object'])
        context['discount'] = get_promo(self.object)
        context['new_price'] = new_price(context['object'].price, context['discount'])
        context['finish_rating'] = rating_good(self.object)
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        good_object = GoodsDB.objects.filter(slug=self.kwargs.get('slug')) \
            .select_related('category') \
            .select_related('brand')
        return good_object

        # .prefetch_related(Prefetch('category', queryset=CategoryDB.objects.filter(from_category__is_active=True).filter(from_category__category=good_object[0].category)))
        # .prefetch_related(Prefetch('brand', queryset=BrandNameDB.objects.filter(from_brand__is_active=True).filter(from_brand__brand=good_object[0].brand)))


class ShowAllGoods(ListView):
    """Full list class of goods"""
    model = GoodsDB
    template_name = 'shopping/shopping.html'
    context_object_name = 'goods'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowAllGoods, self).get_context_data(**kwargs)
        context['filter'] = GoodsFilter(self.request.GET, queryset=context['object_list'])
        context['object_list'] = context['filter'].qs
        context['rating_list'] = rating_list(context['goods'])
        context['new_price_list'] = new_price_list(context['goods'])
        context['show_photo'] = photo_list(context['goods'])
        context['promo_list'] = promo_list(context['goods'])
        if self.request.GET.get('show_as') == 'list':
            context['show_as'] = 'list'
        else:
            context['show_as'] = 'grid'

        return context

    def get_queryset(self):

        if 'slug_cat' in self.kwargs.keys():
            queryset = GoodsDB.objects.filter(presence=True, category__slug=self.kwargs['slug_cat']).select_related('category').select_related('brand')
        elif 'slug_brand' in self.kwargs.keys():
            queryset = GoodsDB.objects.filter(presence=True, brand__slug=self.kwargs['slug_brand']).select_related('category').select_related('brand')
        else:
            queryset = GoodsDB.objects.filter(presence=True).select_related('category').select_related('brand')

        if self.request.GET.get('show_on_page'):
            self.paginate_by = self.request.GET.get('show_on_page')

        if self.request.GET.get('sort_on') == 'popularity':
            result = GoodsFilter(self.request.GET, queryset.order_by('-n_views')).qs.select_related('category').select_related('brand')
        else:
            result = GoodsFilter(self.request.GET, queryset).qs.select_related('category').select_related('brand')
        return result.select_related('category').select_related('brand')




def get_category(request, slug):
    '''тестовая функция просмотра товара по категориям'''
    return render(request, 'shopping/get_category.html', {'hello': f'Hello, category {slug}!'})


def show_image(request, slug):
    '''тестовая функция просмотра картинки'''
    return render(request, 'shopping/show_image.html', {'hello': f'Hello, image {slug}!'})


def get_brand(request, slug):
    '''тестовая функция просмотра товара по производителю'''
    return render(request, 'shopping/brand.html', {'hello': f'Hello, brand {slug}!'})

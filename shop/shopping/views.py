from django.contrib import messages
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import CartAddProductForm
from .models import *
from .forms import AddReviewForm
from .get_func import *
from .filters import GoodsFilter
from main_app.models import *


def shopping_search(request):
    """Search redirect function"""
    if request.GET.get('search_shop') and request.GET.get('next'):
        result = request.GET.get('search_shop')
    else:
        return redirect(request.GET['next'])
    return redirect('search_result', str(result))


class ShowGood(CreateView, DetailView):
    """Single product page class"""
    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'
    form_class = AddReviewForm
    # data_good = ...

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_name = self.request.user
            form.instance.good = GoodsDB.objects.filter(slug=self.kwargs.get('slug')).first()
            return super(ShowGood, self).form_valid(form)
        else:
            raise Http404('Для отправки своего отзыва Вы должны зарегистрироваться или залогиниться')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['data_good'] = self.data_good.show_goods_all
        context['cart_product_form'] = CartAddProductForm()
        by_reviews = ShowObjects.rating_and_reviews_for_one_good(self.object)
        context['reviews'] = by_reviews['reviews_list']
        context['discount'] = self.by_promo[self.object]['discount']
        context['new_price'] = round(self.object.price * self.by_promo[self.object]['discount_index'], 2)
        context['finish_rating'] = by_reviews['int_rating']
        return context

    def get_queryset(self):
        good_object = GoodsDB.objects.filter(slug=self.kwargs.get('slug'))\
            .select_related('category', 'brand').prefetch_related('images_for_goods')
        # self.data_good = ShowObjects(good_object)
        self.by_promo = ShowObjects.promo_dict(good_object)
        return good_object


class ShowAllGoods(ListView):
    """Full list class of goods"""
    template_name = 'shopping/shopping.html'
    context_object_name = 'goods'
    paginate_by = 6
    filters = ...
    data_goods = ...

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowAllGoods, self).get_context_data(**kwargs)
        context['filter'] = self.filters
        context['breadcrumb_list'] = self.request.path[1: -1].split('/')
        context['data_goods'] = self.data_goods.show_goods_all

        if self.request.GET.get('show_as') == 'list':
            context['show_as'] = 'list'

        if 'slug_cat' in self.kwargs.keys():
            context['title'] = f'Товары категории: {CategoryDB.objects.get(slug=self.kwargs["slug_cat"])}'
        elif 'slug_brand' in self.kwargs.keys():
            context['title'] = f'Товары от производителя: {BrandNameDB.objects.get(slug=self.kwargs["slug_brand"])}'
        elif 'search_result' in self.kwargs.keys():
            context['title'] = f'Поиск по: "{self.kwargs["search_result"]}"'
        else:
            context['title'] = 'Все товары'
        return context

    def get_queryset(self):
        if 'slug_cat' in self.kwargs.keys():    # если пришел запрос на показ по категориям
            queryset = GoodsDB.objects.filter(presence=True, category__slug=self.kwargs['slug_cat'])\
                .select_related('category', 'brand')\
                .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')
        elif 'slug_brand' in self.kwargs.keys():    # если пришел запрос на показ по брендам
            queryset = GoodsDB.objects.filter(presence=True, brand__slug=self.kwargs['slug_brand'])\
                .select_related('category', 'brand')\
                .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')
        elif 'search_result' in self.kwargs.keys():     # если проводился поиск
            query = self.kwargs['search_result']
            queryset = GoodsDB.objects.filter(presence=True)\
                .filter(Q(title__icontains=query) | Q(description__icontains=query))\
                .select_related('category', 'brand')\
                .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')
        else:   # дефолтный запрос "Все товары"
            queryset = GoodsDB.objects.filter(presence=True)\
                .select_related('category', 'brand')\
                .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')

        if self.request.GET.get('show_on_page'):
            self.paginate_by = self.request.GET.get('show_on_page')

        self.data_goods = ShowObjects(queryset)     # подключаем класс обработки в get_func

        if self.request.GET.get('sort_on'):     # инициализируем сортировку
            queryset = self.get_queryset_by_sort(queryset)

        self.filters = GoodsFilter(self.request.GET, queryset=None)     # инициализируем фильтр
        return queryset

    def get_queryset_by_sort(self, queryset):

        if self.request.GET.get('sort_on') == 'popularity':
            return queryset.order_by('-n_views')
        elif self.request.GET.get('sort_on') == 'rating':
            return self.data_goods.sort_by_rating
        elif self.request.GET.get('sort_on') == 'price':
            return self.data_goods.sort_by_price
        elif self.request.GET.get('sort_on') == 'price-desc':
            return self.data_goods.sort_by_price_desc
        else:
            return queryset

#
# def show_image(request, slug):
#     """тестовая функция просмотра картинки"""
#     return render(request, 'shopping/show_image.html', {'hello': f'Hello, image {slug}!'})
#

from django.db.models import Prefetch, Q
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

from main_app.models import PromotionDB
from .filters import GoodsFilter
from .forms import AddReviewForm
from orders.forms import CartAddProductForm
from .get_func import ShowObjects, ShowOneObject
from .models import BrandNameDB, CategoryDB, GoodsDB, ReviewsDB


def shopping_search(request):
    """
    The function to display the founded goods
    """

    if request.GET.get('search_shop') and request.GET.get('next'):
        result = request.GET.get('search_shop')
    else:
        return redirect(request.GET['next'])
    return redirect('search_result', str(result))


class ShowGood(CreateView, DetailView):
    """
    Class to display the good's page
    """

    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'
    form_class = AddReviewForm
    data_good = ...

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user_name = self.request.user
            form.instance.good = GoodsDB.objects.filter(
                slug=self.kwargs.get('slug')).first()
            return super(ShowGood, self).form_valid(form)
        else:
            raise Http404(
                'Для отправки своего отзыва Вы должны зарегистрироваться'
                ' или залогиниться')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.data_good = ShowOneObject(self.object)
        context['data_good'] = self.data_good.data_good
        context['cart_product_form'] = CartAddProductForm()
        return context

    def get_queryset(self):
        good_object = GoodsDB.objects.filter(slug=self.kwargs.get('slug')) \
            .select_related('category', 'brand') \
            .prefetch_related('images_for_goods',
                              Prefetch('review_for_good',
                                       queryset=ReviewsDB.objects
                                       .prefetch_related('user_name')),
                              Prefetch('category__from_category',
                                       queryset=PromotionDB.objects.filter(
                                           is_active=True)),
                              Prefetch('brand__from_brand',
                                       queryset=PromotionDB.objects.filter(
                                           is_active=True)),
                              )
        return good_object


class ShowAllGoods(ListView):
    """
    Class to display the full list of goods
    """

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
            context['title'] = f'Товары категории: ' \
                               f'{CategoryDB.objects.get(slug=self.kwargs["slug_cat"])}'
        elif 'slug_brand' in self.kwargs.keys():
            context['title'] = f'Товары бренда: ' \
                               f'{BrandNameDB.objects.get(slug=self.kwargs["slug_brand"])}'
        elif 'search_result' in self.kwargs.keys():
            context['title'] = f'Поиск по: "{self.kwargs["search_result"]}"'
        else:
            context['title'] = 'Все товары'
        return context

    def get_queryset(self):
        if 'slug_cat' in self.kwargs.keys():
            queryset = GoodsDB.objects.filter(presence=True,
                                              category__slug=self.kwargs[
                                                  'slug_cat']) \
                .select_related('category', 'brand') \
                .prefetch_related('images_for_goods',
                                  'review_for_good',
                                  Prefetch('category__from_category',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  Prefetch('brand__from_brand',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  )
        elif 'slug_brand' in self.kwargs.keys():
            queryset = GoodsDB.objects.filter(presence=True,
                                              brand__slug=self.kwargs[
                                                  'slug_brand']) \
                .select_related('category', 'brand') \
                .prefetch_related('images_for_goods',
                                  'review_for_good',
                                  Prefetch('category__from_category',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  Prefetch('brand__from_brand',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  )
        elif 'search_result' in self.kwargs.keys():
            query = self.kwargs['search_result']
            queryset = GoodsDB.objects.filter(presence=True) \
                .filter(
                Q(title__icontains=query) | Q(description__icontains=query)) \
                .select_related('category', 'brand') \
                .prefetch_related('images_for_goods',
                                  'review_for_good',
                                  Prefetch('category__from_category',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  Prefetch('brand__from_brand',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  )
        else:
            queryset = GoodsDB.objects.filter(presence=True) \
                .select_related('category', 'brand') \
                .prefetch_related('images_for_goods',
                                  'review_for_good',
                                  Prefetch('category__from_category',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  Prefetch('brand__from_brand',
                                           queryset=PromotionDB.objects.filter(
                                               is_active=True)),
                                  )

        if self.request.GET.get('show_on_page'):
            self.paginate_by = self.request.GET.get('show_on_page')
        # подключаем класс обработки в get_func
        self.data_goods = ShowObjects(queryset)
        # инициализируем сортировку
        if self.request.GET.get('sort_on'):
            queryset = self.get_queryset_by_sort(queryset)
        # инициализируем фильтр
        self.filters = GoodsFilter(self.request.GET,
                                   queryset=None)
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

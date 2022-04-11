from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import AddReviewForm
from .get_func import *


class ShowGood(LoginRequiredMixin, CreateView, DetailView):
    '''Single product page class'''
    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'
    form_class = AddReviewForm

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.instance.good = GoodsDB.objects.filter(slug=self.kwargs.get('slug')).first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.filter(product=context['object'])
        context['reviews'] = ReviewsDB.objects.filter(good=context['object'])
        context['new_price'] = new_price(context['object'].price)
        context['finish_rating'] = rating_good(self.object)
        return context


class ShowAllGoods(ListView):
    '''Full list class of goods'''
    model = GoodsDB
    template_name = 'shopping/shopping.html'
    context_object_name = 'goods'
    paginate_by = 12

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowAllGoods, self).get_context_data(**kwargs)
        context['rating_list'] = rating_list(context['goods'])
        context['new_price_list'] = new_price_list(context['goods'])
        context['show_photo'] = photo_list(context['goods'])

        return context

    def get_queryset(self):
        '''используем, чтобы вывести только те товары, которые помечены, как наличные в магазине'''
        return GoodsDB.objects.filter(presence=True)






def shopping(request):
    '''тестовая функция обработки покупки заказа'''
    return render(request, 'shopping/shopping.html', {'hello': 'Hello, shop!'})


def get_category(request, slug):
    '''тестовая функция просмотра товара по категориям'''
    return render(request, 'shopping/get_category.html', {'hello': f'Hello, category {slug}!'})


def show_image(request, slug):
    '''тестовая функция просмотра картинки'''
    return render(request, 'shopping/show_image.html', {'hello': f'Hello, image {slug}!'})


def get_brand(request, slug):
    '''тестовая функция просмотра товара по производителю'''
    return render(request, 'shopping/brand.html', {'hello': f'Hello, brand {slug}!'})


# def show_good(request, slug):
#     '''тестовая функция просмотра товара по производителю'''
#     return render(request, 'shopping/show_good.html', {'hello': f'Hello, good {slug}!'})

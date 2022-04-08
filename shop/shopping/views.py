from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import admin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import AddReviewForm


class ShowGood(DetailView):
    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'

    @staticmethod
    def add_review(request):
        if request.user.is_authenticated:
            review_title = request.GET.get('review_title')
            user_name = request.user
            text = request.GET.get('review_text')
            good = object
            rating = request.GET.get('review_rating')

            data = {'review_title': review_title, 'user_name': user_name, 'text': text, 'good': good, 'rating': rating}
            ReviewsDB.objects.create(**data)
        return redirect('good', object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.filter(product=context['object'])
        context['reviews'] = ReviewsDB.objects.filter(good=context['object'])
        context['new_price'] = int(context['object'].price * 0.75)
        # context['add_review'] = self.add_review(self.request)
        # for i in context:
        #     print(i)
        # print(context['view'])
        # if self.request:
        #     print(self.request)
        #     self.add_review()
        return context


class CreateReview(DetailView):
    model = GoodsDB
    template_name = 'shopping/show_good.html'
    context_object_name = 'good_item'

    def get_context_data(self, **kwargs):
        context = super(CreateReview, self).get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.filter(product=context['object'])
        context['reviews'] = ReviewsDB.objects.filter(good=context['object'])
        context['new_price'] = int(context['object'].price * 0.75)

        if self.request.user.is_authenticated:
            review_title = self.request.GET.get('review_title')
            user_name = self.request.user
            text = self.request.GET.get('review_text')
            good = self.object
            rating = self.request.GET.get('review_rating')

            data = {'review_title': review_title, 'user_name': user_name, 'text': text, 'good': good, 'rating': rating}
            ReviewsDB.objects.create(**data)

        return context


class ShowAllGoods(ListView):
    model = GoodsDB
    template_name = 'shopping/shopping.html'
    context_object_name = 'goods'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowAllGoods, self).get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.all()
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

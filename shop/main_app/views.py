from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from shopping.models import GoodsDB, GalleryDB


class MainPageView(TemplateView):
    """doc string"""
    model = GoodsDB
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


"""
в shopping/shopping.html
{% empty %}
<p>По Вашему запросу ничего не найдено</p>
"""


class SearchGoodView(ListView):
    """doc string"""
    model = GoodsDB
    template_name = 'shopping/shopping.html' #shopping.html
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hello'] = 'Найденные товары'
        # context['q'] = f"q={self.request.GET.get('q')}&"
        return context

    def get_queryset(self):
        return GoodsDB.objects.filter(title__icontains=self.request.GET.get('q'))



# TODO переделать
class PromotionOneView(ListView):
    """doc string"""
    model = GoodsDB
    template_name = 'shopping/category.html' #shopping.html
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.all()
        context['hello'] = 'Выгодные предложения'
        return context

    def get_queryset(self):
        return GoodsDB.objects.filter(price__gte=299)

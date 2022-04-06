from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from shopping.models import GoodsDB, GalleryDB


class SearchGoodView(ListView):
    """doc string"""
    model = GoodsDB
    template_name = 'shopping/shopping.html'
    context_object_name = 'good'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = GalleryDB.objects.all()
        context['title'] = 'Найденные товары'
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        return GoodsDB.objects.filter(title__icontains=query)


class MainPageView(TemplateView):
    """doc string"""
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class BlogView(TemplateView):
    """doc string"""
    template_name = 'main_app/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        return context


class AboutView(TemplateView):
    """doc string"""
    template_name = 'main_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        return context


class ContactView(TemplateView):
    """doc string"""
    template_name = 'main_app/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Свяжитесь с нами'
        return context


class PaymentView(TemplateView):
    """doc string"""
    template_name = 'main_app/payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Способы оплаты'
        return context


class DeliveryView(TemplateView):
    """doc string"""
    template_name = 'main_app/delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доставка'
        return context


class FAQsView(TemplateView):
    """doc string"""
    template_name = 'main_app/faqs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Часто задаваемые вопросы'
        return context


class SupportView(TemplateView):
    """doc string"""
    template_name = 'main_app/support.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поддержка'
        return context


class PrivacyView(TemplateView):
    """doc string"""
    template_name = 'main_app/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Конфиденциальность'
        return context


class WarrantyView(TemplateView):
    """doc string"""
    template_name = 'main_app/warranty.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Гарантии'
        return context


class ConditionsView(TemplateView):
    """doc string"""
    template_name = 'main_app/conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Условия и положения'
        return context


class ReturnView(TemplateView):
    """doc string"""
    template_name = 'main_app/return.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Возврат'
        return context


class IntellPropertyView(TemplateView):
    """doc string"""
    template_name = 'main_app/intellproperty.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Интеллектуальная собственность'
        return context



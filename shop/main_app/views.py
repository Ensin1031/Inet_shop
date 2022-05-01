from django.views.generic import TemplateView

from orders.cart import Cart
from shopping.views import ShowAllGoods
from shopping.get_func import *
from shopping.filters import GoodsFilter


class MainPageView(TemplateView):
    """doc string"""
    model = GoodsDB
    template_name = 'main_app/index.html'


# todo search get q
class SearchGoodView(ShowAllGoods):
    """doc string"""

    def get_queryset(self):
        search = self.request.GET.get('q')
        return GoodsDB.objects.filter(presence=True, title__icontains=search)


class CartShowView(TemplateView):
    """"""
    template_name = 'inc/_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context


class PromotionView(ShowAllGoods):
    """doc string"""
    model = GoodsDB

    def get_queryset(self):
        queryset = super().get_queryset()
        active_promo = PromotionDB.objects.filter(slug=self.kwargs.get('slug_promo'))
        for promo in active_promo:
            good_filter = Q(category__in=[cat.id for cat in promo.category.all()]) \
                          | Q(brand__in=[brand.id for brand in promo.brand.all()])
            queryset = GoodsDB.objects.filter(presence=True).filter(good_filter)

        return queryset

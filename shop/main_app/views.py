from django.db.models import Q
from django.views.generic import TemplateView

from main_app.models import PromotionDB
from orders.cart import Cart
from shopping.models import GoodsDB
from shopping.views import ShowAllGoods


class MainPageView(TemplateView):
    """
    Class to display the main page
    """

    model = GoodsDB
    template_name = 'main_app/index.html'


# todo search get q
class SearchGoodView(ShowAllGoods):
    """doc string"""

    def get_queryset(self):
        search = self.request.GET.get('q')
        return GoodsDB.objects.filter(presence=True, title__icontains=search)


class CartShowView(TemplateView):
    """
    Class to display the cart
    """

    template_name = 'inc/_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context


class PromotionView(ShowAllGoods):
    """
    Class to display promotion goods
    """

    model = GoodsDB

    def get_queryset(self):
        queryset = super().get_queryset()
        active_promo = PromotionDB.objects.filter(
                slug=self.kwargs.get('slug_promo')
        )
        for promo in active_promo:
            goods = Q(category__in=[cat.id for cat in promo.category.all()]) \
                    | Q(brand__in=[brand.id for brand in promo.brand.all()])
            queryset = GoodsDB.objects.filter(presence=True).filter(goods)
        if self.request.GET.get('sort_on'):
            queryset = self.get_queryset_by_sort(queryset)
        return queryset

from django.views.generic import TemplateView

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


class PromotionView(ShowAllGoods):
    """doc string"""

    def get_queryset(self):
        active_promo = PromotionDB.objects.filter(slug=self.kwargs.get('slug_promo'))
        for promo in active_promo:
            good_filter = Q(category__in=[cat.id for cat in promo.category.all()]) \
                          | Q(brand__in=[brand.id for brand in promo.brand.all()])
            queryset = GoodsDB.objects.filter(presence=True).filter(good_filter)

        result = GoodsFilter(self.request.GET, queryset).qs
        return result

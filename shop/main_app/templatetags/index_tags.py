from django import template
from django.db.models import Prefetch

from main_app.models import PromotionDB
from shopping.get_func import ShowObjects
from shopping.models import BrandNameDB, CategoryDB, GoodsDB

register = template.Library()


@register.inclusion_tag('inc/_submenu.html')
def show_submenu():
    """The function to show submenu in header"""

    categories = CategoryDB.objects.all()
    brands = BrandNameDB.objects.all()

    count = {
        'categories': categories,
        'brands': brands,
    }

    return count


@register.inclusion_tag('inc/_promo.html')
def show_promo():
    """The function for show promotions on the main page"""

    promotions = PromotionDB.objects.filter(is_active=True)\
        .prefetch_related('category', 'brand')
    cat_promo = {}
    brand_promo = {}

    for promo in promotions:
        for cat in promo.category.all():
            cat_promo.setdefault(promo, []).append(cat.title)
        for brand in promo.brand.all():
            brand_promo.setdefault(promo, []).append(brand.title)

    count = {
        'promotions': promotions,
        'cat_promo': cat_promo,
        'brand_promo': brand_promo,
    }

    return count


@register.inclusion_tag('inc/_fav_goods.html')
def show_fav_goods():
    """The function for show favorite goods on the main page"""

    goods = GoodsDB.objects.filter(presence=True).order_by('-n_views')[:9] \
        .select_related('category', 'brand') \
        .prefetch_related('images_for_goods',
                          'review_for_good',
                          Prefetch('category__from_category',
                                   queryset=PromotionDB.objects.filter(
                                           is_active=True
                                   )),
                          Prefetch('brand__from_brand',
                                   queryset=PromotionDB.objects.filter(
                                           is_active=True
                                   )),
                          )
    data_goods = ShowObjects(goods)

    count = {
        'goods': goods,
        'goods_dict': data_goods.show_goods_all,
    }

    return count

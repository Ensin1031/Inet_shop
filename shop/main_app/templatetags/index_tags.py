from django import template

from shopping.get_func import *


register = template.Library()


@register.inclusion_tag('inc/_submenu.html')
def show_submenu():
    """"""
    categories = CategoryDB.objects.all()
    brands = BrandNameDB.objects.all()

    count = {
        'categories': categories,
        'brands': brands,
    }

    return count


@register.inclusion_tag('inc/_promo.html')
def show_promo():
    """"""
    promotions = PromotionDB.objects.filter(is_active=True)
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
        'brand_promo': brand_promo
    }

    return count


# TODO
@register.inclusion_tag('inc/_fav_goods.html')
def show_fav_goods(category=None):
    """"""
    if category == None:
        goods = GoodsDB.objects.filter(presence=True).order_by('-n_views')[:9]
    else:
        goods = GoodsDB.objects.filter(presence=True).filter(
            category=category).order_by('-n_views')[:9]
    count = {
        'goods': goods,
        'show_photo': photo_list(goods),
        'show_new_price': new_price_list(goods),
        'show_rating': rating_list(goods),
        'promo_list': promo_list(goods)
    }
    return count





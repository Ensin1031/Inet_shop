from django import template
from django.db.models import Sum, Count

from shopping.models import GalleryDB, GoodsDB, CategoryDB, ReviewsDB, BrandNameDB
from shopping.get_func import *


register = template.Library()


@register.inclusion_tag('inc/_goods_band.html')
def show_band(category=None):
    '''show best products band'''
    if category == None:
        goods = GoodsDB.objects.filter(presence=True).order_by('-n_views')[:8]
    else:
        goods = GoodsDB.objects.filter(presence=True).filter(category=category).order_by('-n_views')[:8]
    count = {
        'goods': goods,
        'show_photo': photo_list(goods),
        'show_new_price': new_price_list(goods),
        'show_rating': rating_list(goods),
    }
    return count


@register.inclusion_tag('inc/_shop_sidebar.html')
def show_sidebar():
    '''show sidebar on the shopping app'''
    goods = GoodsDB.objects.filter(presence=True).order_by('-n_views')[:6]
    category = category_by_count()
    count = {
        'goods': goods,
        'show_photo': photo_list(goods),
        'show_new_price': new_price_list(goods),
        'show_rating': rating_list(goods),
        'brands': brand_by_count(),
        'category': category[0],
        'category_count': category[1],
    }
    return count

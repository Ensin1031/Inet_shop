from django import template
from django.db.models import Count, F
from django.utils.http import urlencode

from shopping.models import GalleryDB, GoodsDB, CategoryDB, ReviewsDB, BrandNameDB
from shopping.get_func import *

register = template.Library()


@register.inclusion_tag('inc/_goods_band.html')
def show_band(good):
    '''show the best products band'''
    goods = good.category.category_good.filter(presence=True)\
        .filter(category=good.category).order_by('-n_views')[:8].select_related('category', 'brand')\
        .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')
    show_goods = ShowObjects(goods)
    count = {
        'goods': goods,
        'goods_dict': show_goods.show_goods_all,
    }
    return count


@register.inclusion_tag('inc/_shop_sidebar.html')
def show_sidebar(request):
    '''show sidebar on the shopping app'''
    goods = GoodsDB.objects.filter(presence=True)\
        .order_by('-n_views')[:6].select_related('category', 'brand')\
        .prefetch_related('images_for_goods', 'review_for_good', 'category__from_category', 'brand__from_brand')
    data_goods = ShowObjects(goods)
    count = {
        'goods': goods,
        'goods_dict': data_goods.show_goods_all,
        'brands': BrandNameDB.objects.annotate(cnt=Count('brand_good', filter=F('brand_good__presence'))),
        'category': CategoryDB.objects.annotate(cnt=Count('category_good', filter=F('category_good__presence'))),
        'request': request,
    }
    return count


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

from django import template
from django.db.models import Sum, Count

from shopping.models import GalleryDB, GoodsDB, CategoryDB, ReviewsDB

register = template.Library()


@register.inclusion_tag('inc/_goods_band.html')
def show_band():
    '''show best products band'''
    goods = GoodsDB.objects.filter(presence=True).order_by('-n_views')[:8]

    show_new_price = {}
    show_photo = {}
    show_rating = {}

    for good in goods:
        show_photo[good] = good.images_for_goods.first()
        show_new_price[good] = int(int(good.price) * 0.75)

        zn = good.review_for_good.filter(good=good).aggregate(Count('review_rating'))
        if zn['review_rating__count'] > 0:
            show_rating[good] = 0

            for value in good.review_for_good.filter(good=good):
                show_rating[good] += int(value.review_rating)

            show_rating[good] = int(show_rating[good] / zn['review_rating__count'])
        else:
            show_rating[good] = 0

    count = {
        'goods': goods,
        'show_photo': show_photo,
        'show_new_price': show_new_price,
        'show_rating': show_rating,
    }

    return count

import django_filters

from .get_func import *


class GoodsFilter(django_filters.FilterSet):
    """Implementation of sorting fields on the main page of the store"""
    CHOICES_SORT = (
        ('popularity', 'Сортировка по популярности'),
        ('rating', 'Сортировка по рейтингу'),
        ('price', 'Сортировка по цене: по возрастанию'),
        ('price-desc', 'Сортировка по цене: по убыванию'),
    )
    CHOICES_SHOW_ON = (
        ('9', '9'),
        ('12', '12'),
        ('15', '15'),
        ('18', '18'),
    )
    CHOICES_SHOW_AS = (
        ('grid', 'Сетка'),
        ('list', 'Список'),
    )

    sort_on = django_filters.ChoiceFilter(
        label='Сортировать по:',
        choices=CHOICES_SORT,
        method='show_sort_list',
    )

    show_on_page = django_filters.ChoiceFilter(
        label='Товаров на странице:',
        choices=CHOICES_SHOW_ON,
        method='show_sort_list',
    )
    show_as = django_filters.ChoiceFilter(
        label='Показать в виде:',
        choices=CHOICES_SHOW_AS,
        method='show_sort_list',
    )

    class Meta:
        model = GoodsDB
        fields = ()

    @staticmethod
    def show_sort_list(queryset, name, value):
        if value == 'popularity':
            result = queryset.order_by('-n_views')
        elif value == 'rating':
            result = sort_on_rating(queryset)
        elif value == 'price':
            result = sort_on_price(queryset)
        elif value == 'price-desc':
            result = sort_on_price_desc(queryset)
        else:
            result = queryset
        return result


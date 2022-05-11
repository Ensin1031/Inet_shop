import django_filters

from .get_func import *


class GoodsFilter(django_filters.FilterSet):
    """
    Class implementing the sorting fields on the main page of the shop
    """

    CHOICES_SORT = (
        ('popularity', 'популярность'),
        ('rating', 'рейтинг'),
        ('price', 'цена: по возрастанию'),
        ('price-desc', 'цена: по убыванию'),
    )
    CHOICES_SHOW_ON = (
        ('9', '9'),
        ('12', '12'),
        ('15', '15'),
        ('18', '18'),
        ('21', '21'),
    )
    CHOICES_SHOW_AS = (
        ('grid', 'Сетка'),
        ('list', 'Список'),
    )

    sort_on = django_filters.ChoiceFilter(
            label='Сортировать по:',
            choices=CHOICES_SORT,
    )
    show_on_page = django_filters.ChoiceFilter(
            label='Товаров на странице:',
            choices=CHOICES_SHOW_ON,
    )
    show_as = django_filters.ChoiceFilter(
            label='Показать в виде:',
            choices=CHOICES_SHOW_AS,
    )

    class Meta:
        model = GoodsDB
        fields = ()

    @staticmethod
    def show_sort_list(queryset, name, value):
        pass

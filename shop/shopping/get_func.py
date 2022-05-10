from django.db.models import Q, Case, When, Prefetch

from .models import *
from main_app.models import *


class ShowObjects:
    """
    Request objects processing class.
    """

    def __init__(self, obj_list):
        self.obj_list = obj_list

        self.rating_dict_all = self.rating_dict(self.obj_list)
        self.promo_dict_all = self.promo_dict(self.obj_list)
        self.new_price_dict_all = self.new_price_dict(self.obj_list)
        self.sort_by_rating = self.sort_on_rating()
        self.sort_by_price = self.sort_on_price()
        self.sort_by_price_desc = self.sort_on_price_desc()
        self.show_goods_all = self.show_goods(self.obj_list)

    def show_goods(self, object_list):
        """The function of processing a list of objects and converting them to JSON form"""
        result = {}
        if object_list:
            for good in object_list:
                result[str(good.id)] = {
                    'product': good,
                    'new_price': self.new_price_dict_all[good],
                    'rating': self.rating_dict_all[good],
                    'promo': self.promo_dict_all[good]['discount'],
                }
        return result

    @staticmethod
    def rating_dict(good_list):
        """
        The function calculates the average value of ratings for a list of products.

        функция высчитывает среднее значение рейтингов для списка товаров

        принимает: список объектов из GoodsDB

        возвращает: словарь вида
        {<объект_GoodsDB_№1>: <int(1-100)_процентов_для_GoodsDB_№1>,
        <объект_GoodsDB_№2>: <int(1-100)_процентов_для_GoodsDB_№2>,... }
        """
        rating = {}
        for item in good_list:
            rating_for_good = item.review_for_good.all()
            if rating_for_good:
                len_rating = len(rating_for_good)
                sum_rating = 0
                for value in rating_for_good:
                    sum_rating += int(value.review_rating)
                result = int(sum_rating / len_rating)
            else:
                result = 0
            rating[item] = result
        return rating

    @staticmethod
    def promo_dict(good_list):
        """
        Функция высчитывает данные по скидкам для списка товаров из GoodsDB

        принимает: список объектов из GoodsDB

        возвращает: словарь вида
        {
        <объект_GoodsDB_№1>: {'discount_index': <float_значение(0.01-1)>, 'discount': <int(1-100)>}
        <объект_GoodsDB_№2>: {'discount_index': <float_значение(0.01-1)>, 'discount': <int(1-100)>}
        }
                где:
            'discount_index' - индекс от 0.01 до 1 для высчитывания новой цены, если скидки отсутствуют = 1
            'discount' - в процентах, значение скидки для товара, максимальное из найденных, если отсутствует = None
        """
        promo = {}
        for item in good_list:
            queryset_for_good_by_category = item.category.from_category.all()
            queryset_for_good_by_brand = item.brand.from_brand.all()
            discount_list = []
            if queryset_for_good_by_category:
                for value in queryset_for_good_by_category:
                    discount_list.append(abs(value.discount))

            if queryset_for_good_by_brand:
                for value in queryset_for_good_by_brand:
                    discount_list.append(abs(value.discount))
            if discount_list:
                discount_index = 1 - max(discount_list)
                discount = int(max(discount_list) * 100)
                result = {'discount_index': discount_index, 'discount': discount}
            else:
                result = {'discount_index': 1, 'discount': None}
            promo[item] = result
        return promo

    def new_price_dict(self, good_list):
        price = {}
        for obj in good_list:
            price[obj] = round(self.promo_dict_all[obj]['discount_index'] * obj.price, 2)
        return price

    @staticmethod
    def __sort_base_funk(goods_dict, rev=True):
        """
        Базовая функция сортировки

        получает: словарь типа
        {<объект_GoodsDB_№1>: <int(0-100)_для_GoodsDB_№1>, <объект_GoodsDB_№2>: <int(0-100)_для_GoodsDB_№2>,... }
        вторым аргументом - булевое значение реверса сортировки, по умолчанию =True

        возвращает: <QuerySet[отсортированный список]>
        """
        result = list(dict(sorted(goods_dict.items(), key=lambda x: x[1], reverse=rev)).keys())
        pk_list = [x.pk for x in result]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = GoodsDB.objects.filter(pk__in=pk_list).order_by(preserved)\
            .select_related('category', 'brand')\
            .prefetch_related('images_for_goods',
                              Prefetch('review_for_good', queryset=ReviewsDB.objects.prefetch_related('user_name')),
                              Prefetch('category__from_category', queryset=PromotionDB.objects.filter(is_active=True)),
                              Prefetch('brand__from_brand', queryset=PromotionDB.objects.filter(is_active=True)),
                              )
        return queryset

    def sort_on_rating(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по рейтингу + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров
        """
        rating_dict = self.rating_dict_all
        return self.__sort_base_funk(rating_dict)

    def sort_on_price(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
        по возрастанию + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров по цене по возрастанию
        """
        price_dict = self.new_price_dict_all
        return self.__sort_base_funk(price_dict, False)

    def sort_on_price_desc(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
        по убыванию + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров по цене по убыванию
        """
        price_dict = self.new_price_dict_all
        return self.__sort_base_funk(price_dict)


class ShowOneObject:

    def __init__(self, good):
        self.good = good

        self.promo = self.__good_promo(self.good)
        self.rating = self.__rating(self.good)
        self.data_good = self.show_good(self.good)

    def show_good(self, good):
        result = {
            'product': good,
            'new_price': round(self.promo['discount_index'] * good.price, 2),
            'rating': self.rating['int_rating'],
            'review_list': self.rating['reviews_list'],
            'promo': self.promo['discount'],
        }
        return result

    @staticmethod
    def __good_promo(good):
        queryset_for_good_by_category = good.category.from_category.all()
        queryset_for_good_by_brand = good.brand.from_brand.all()
        discount_list = []
        if queryset_for_good_by_category:
            for value in queryset_for_good_by_category:
                discount_list.append(abs(value.discount))

        if queryset_for_good_by_brand:
            for value in queryset_for_good_by_brand:
                discount_list.append(abs(value.discount))

        if discount_list:
            discount_index = 1 - max(discount_list)
            discount = int(max(discount_list) * 100)
            result = {'discount_index': discount_index, 'discount': discount}
        else:
            result = {'discount_index': 1, 'discount': None}

        return result

    @staticmethod
    def __rating(good):
        """
        The function of processing data from the ReviewsDB database for one product.

        получает: 1 объект GoodsDB

        возвращает: словарь вида {'int_rating': <int(0-100)_процентов>, 'reviews_list': <queryset>}
                где:
            'int_rating' - рейтинг товара в процентах, с учетом всех отзывов, если отзывы отсутствуют = 0
            'reviews_list' - список объектов отзывов, относящихся к данному товару, если он отсутствует = None
        """
        queryset_rating_for_good = good.review_for_good.all()  # .prefetch_related('user_name')
        if queryset_rating_for_good:
            len_queryset = queryset_rating_for_good.count()
            sum_rating = 0
            for value in queryset_rating_for_good:
                sum_rating += int(value.review_rating)
            result = {'int_rating': int(sum_rating / len_queryset), 'reviews_list': queryset_rating_for_good}
        else:
            result = {'int_rating': 0, 'reviews_list': None}
        return result


def get_promo(good):
    """
    Функция получения информации о скидках на данный товар

    принимает: 1 объект GoodsDB

    возвращает: float(значение)
    """
    promo = PromotionDB.objects.filter(is_active=True).filter(Q(category=good.category) | Q(brand=good.brand))
    discount = list()
    if promo:
        for obj in promo:
            discount.append(obj.discount)
        result = 1 - max(discount)
    else:
        result = 1
    return result

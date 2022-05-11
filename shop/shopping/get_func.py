from django.db.models import Q, Case, When, Prefetch

from .models import *
from main_app.models import *


class ShowObjects:
    """
    Class to process the requested objects
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
        """
        The function to process a list of objects
        and converting it to JSON form
        """

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
        The function calculates the average rating for a list of goods

        :param good_list: list of goods from database
        :type good_list: list

        :return: dictionary of ratings for corresponding goods
        :rtype: dict
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
        The function calculates the discount values for a list of goods

        :param good_list: list of goods from database
        :type good_list: list

        :return: dictionary of discount values and ratios for
                 corresponding goods
        :rtype: dict
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
                result = {'discount_index': discount_index,
                          'discount': discount}
            else:
                result = {'discount_index': 1, 'discount': None}
            promo[item] = result
        return promo

    def new_price_dict(self, good_list):
        """
        The function calculates the prices including discount
        for a list of goods

        :param good_list: list of goods from database
        :type good_list: list

        :return: dictionary of new prices for corresponding goods
        :rtype: dict
        """
        price = {}

        for obj in good_list:
            price[obj] = round(
                self.promo_dict_all[obj]['discount_index'] * obj.price, 2
            )
        return price

    @staticmethod
    def __sort_base_funk(goods_dict, rev=True):
        """
        Main sorting function

        :param goods_dict: dictionary of goods from database,
                           containing numeric data for sorting goods
        :type goods_dict: dict

        :param rev: reverse order of sorting
        :type rev: bool

        :return: sorted goods
        :rtype: QuerySet
        """

        result = list(dict(sorted(goods_dict.items(), key=lambda x: x[1],
                                  reverse=rev)).keys())
        pk_list = [x.pk for x in result]
        preserved = Case(
            *[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = GoodsDB.objects.filter(pk__in=pk_list).order_by(preserved) \
            .select_related('category', 'brand') \
            .prefetch_related('images_for_goods',
                              Prefetch('review_for_good',
                                       queryset=ReviewsDB.objects
                                       .prefetch_related('user_name')),
                              Prefetch('category__from_category',
                                       queryset=PromotionDB.objects.filter(
                                           is_active=True)),
                              Prefetch('brand__from_brand',
                                       queryset=PromotionDB.objects.filter(
                                           is_active=True)),
                              )
        return queryset

    def sort_on_rating(self):
        """
        The function to return list of goods sorted by the rating
        """

        rating_dict = self.rating_dict_all
        return self.__sort_base_funk(rating_dict)

    def sort_on_price(self):
        """
        The function to return list of goods sorted ascending by the price
        including discount value
        """

        price_dict = self.new_price_dict_all
        return self.__sort_base_funk(price_dict, False)

    def sort_on_price_desc(self):
        """
        The function to return list of goods sorted descending by the price
        including discount value
        """

        price_dict = self.new_price_dict_all
        return self.__sort_base_funk(price_dict)


class ShowOneObject:
    """
    Class to process the requested object
    """

    def __init__(self, good):
        self.good = good
        self.promo = self.__good_promo(self.good)
        self.rating = self.__rating(self.good)
        self.data_good = self.show_good(self.good)

    def show_good(self, good):
        """
        The function to process the object
        and converting it to JSON form
        """

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
        """
        The function calculates the discount value for a given goods

        :param good: good
        :type good: object of GoodsDB

        :return: dictionary of discount value and ratio for
                 given good
        :rtype: dict
        """

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
        The function to calculate the rating of given good
        based on data from the ReviewsDB

        :param good: good
        :type good: object of GoodsDB

        :return: dictionary containing rating and list of reviews for
                 given good
        :rtype: dict
        """

        queryset_rating_for_good = good.review_for_good.all()

        if queryset_rating_for_good:
            len_queryset = queryset_rating_for_good.count()
            sum_rating = 0
            for value in queryset_rating_for_good:
                sum_rating += int(value.review_rating)
            result = {'int_rating': int(sum_rating / len_queryset),
                      'reviews_list': queryset_rating_for_good}
        else:
            result = {'int_rating': 0, 'reviews_list': None}
        return result


def get_promo(good):
    """
    The function returns the discount ratio for a given goods

    :param good: good
    :type good: object of GoodsDB

    :return: discount ratio
    :rtype: float
    """

    promo = PromotionDB.objects.filter(is_active=True).filter(
        Q(category=good.category) | Q(brand=good.brand))
    discount = list()

    if promo:
        for obj in promo:
            discount.append(obj.discount)
        result = 1 - max(discount)
    else:
        result = 1
    return result

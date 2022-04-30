from django.db.models import Q, Case, When, Prefetch

from .models import *
from main_app.models import *


rating_all = ReviewsDB.objects.all()
promo_all = PromotionDB.objects.all()   # \
    # .prefetch_related('category')\
    # .prefetch_related('brand')


class ShowObjects:

    full_promo = PromotionDB.objects.all()  # .prefetch_related('category', 'brand')
    full_photo = GalleryDB.objects.all()    # .prefetch_related('product')

    def __init__(self, obj_list):
        # obj_list.prefetch_related('images_for_goods')
        self.obj_list = obj_list
        # self.obj_list.prefetch_related('images_for_goods')
        self.rating_dict_all = self.rating_dict(self.obj_list)
        self.promo_dict_all = self.promo_dict(self.obj_list)
        self.new_price_dict_all = self.new_price_dict(self.obj_list)
        self.photo_dict_all = self.photo_dict(self.obj_list)
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
                    'photo': self.photo_dict_all[good],
                    'new_price': self.new_price_dict_all[good],
                    'rating': self.rating_dict_all[good],
                    'promo': self.promo_dict_all[good]['discount'],
                }
        # for k, v in result.items():
        #     print(k, '=', v)
        return result

    @staticmethod
    def rating_and_reviews_for_one_good(good):
        queryset_rating_for_good = good.review_for_good.prefetch_related('user_name')
        if queryset_rating_for_good:
            len_queryset = queryset_rating_for_good.count()
            sum_rating = 0
            for value in queryset_rating_for_good:
                sum_rating += int(value.review_rating)
            result = {'int_rating': int(sum_rating / len_queryset), 'reviews_list': queryset_rating_for_good}
        else:
            result = {'int_rating': 0, 'reviews_list': None}
        return result

    @staticmethod
    def rating(good):
        queryset_rating_for_good = good.review_for_good.values('review_rating').prefetch_related('user_name')
        if queryset_rating_for_good:
            len_queryset = queryset_rating_for_good.count()
            sum_rating = 0
            for value in queryset_rating_for_good:
                sum_rating += int(value['review_rating'])
            result = int(sum_rating / len_queryset)
        else:
            result = 0
        return result

    def photo_dict(self, good_list):
        photo = {}
        for item in good_list:
            photo[item] = item.images_for_goods.first()
        return photo

    def rating_dict(self, good_list):
        rating = {}
        for item in good_list:
            rating[item] = self.rating(item)
        return rating

    def promo_dict(self, good_list):
        promo = {}
        for item in good_list:
            promo[item] = self.promo(item)
        return promo

    def new_price_dict(self, good_list):
        price = {}
        for obj in good_list:
            price[obj] = round(self.promo_dict_all[obj]['discount_index'] * obj.price, 2)
        return price

    # @staticmethod
    # def promo(good):
    #     queryset_for_good_by_category = good.category.from_category.filter(is_active=True).values('discount')
    #     queryset_for_good_by_brand = good.brand.from_brand.filter(is_active=True).values('discount')
    #     discount_list = []
    #     if queryset_for_good_by_category:
    #         for value in queryset_for_good_by_category:
    #             discount_list.append(abs(value['discount']))
    #
    #     if queryset_for_good_by_brand:
    #         for value in queryset_for_good_by_brand:
    #             discount_list.append(abs(value['discount']))
    #
    #     if discount_list:
    #         discount_index = 1 - max(discount_list)
    #         discount = int(max(discount_list) * 100)
    #         result = {'discount_index': discount_index, 'discount': discount,}
    #     else:
    #         result = {'discount_index': 0, 'discount': None,}
    #     return result

    @staticmethod
    def promo(good):
        queryset_promo = ShowObjects.full_promo.filter(is_active=True).filter(Q(category=good.category) | Q(brand=good.brand)).values('discount')
        discount_list = []
        # if queryset_promo:
        for value in queryset_promo:
            discount_list.append(abs(value['discount']))

        if discount_list:
            discount_index = 1 - max(discount_list)
            discount = int(max(discount_list) * 100)
            result = {'discount_index': discount_index, 'discount': discount, }
        else:
            result = {'discount_index': 1, 'discount': None, }
        return result

    @staticmethod
    def sort_base_funk(goods_dict, rev=True):
        """
        Базовая функция сортировки

        получает: словарь типа
        {<объект_GoodsDB_№1>: <int(1-100)_значение_для_GoodsDB_№1>, <объект_GoodsDB_№2>: <int(1-100)_значение_для_GoodsDB_№2>,... }
        вторым аргументом - булевое значение реверса сортировки, по умолчанию =True

        возвращает: <QuerySet[отсортированный список]>
        """
        result = list(dict(sorted(goods_dict.items(), key=lambda x: x[1], reverse=rev)).keys())
        pk_list = [x.pk for x in result]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = GoodsDB.objects.filter(pk__in=pk_list).order_by(preserved).select_related('category', 'brand')
        return queryset

    def sort_on_rating(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по рейтингу + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров
        """
        rating_dict = self.rating_dict_all
        return self.sort_base_funk(rating_dict)

    def sort_on_price(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
        по возрастанию + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров по цене по возрастанию
        """
        price_dict = self.new_price_dict_all
        return self.sort_base_funk(price_dict, False)

    def sort_on_price_desc(self):
        """
        функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
        по убыванию + параметру наличия в магазине

        принимает: список объектов из GoodsDB

        возвращает: отсортированный список товаров по цене по убыванию
        """
        price_dict = self.new_price_dict_all
        return self.sort_base_funk(price_dict)


# .prefetch_related(Prefetch('category', queryset=CategoryDB.objects.filter(from_category__is_active=True).filter(from_category__category=good_object[0].category)))
# .prefetch_related(Prefetch('brand', queryset=BrandNameDB.objects.filter(from_brand__is_active=True).filter(from_brand__brand=good_object[0].brand)))


def rating_good(good):
    """
    final rating for one good
    функция высчитывает среднее значение рейтинга для ОДНОГО товара

    принимает: 1 объект товара из GoodsDB

    возвращает: int(значение)
    """
    pre_rating = rating_all.filter(good=good)
    len_rating = pre_rating.count()

    if len_rating > 0:
        sum_rating = 0
        for value in pre_rating:
            sum_rating += int(value.review_rating)
        result = int(sum_rating / len_rating)
        rating = result
    else:
        rating = 0

    return rating


def new_price(old_price, discount=1):
    """
    функция высчитывает новыю цену за товар, на данный момент условная скидка - 25%.
    В дальнейшем планируется переделать данную функцию, с учетом привязки поля модели товара "скидки"

    принимает: int(значение) + (если необходимо)индекс скидки

    возвращает: int(значение)
    """
    return round(old_price * discount, 2)


def rating_list(good_list):
    """
    функция высчитывает среднее значение рейтингов для списка товаров

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <среднее_значение_рейтинга>,<объект_GoodsDB_№2>: <среднее_значение_рейтинга>,... }
    """
    rating = {}
    for item in good_list:
        rating[item] = rating_good(item)
    return rating


def new_price_list(goods):
    """
    функция высчитывает новую цену для списка товаров из GoodsDB
    В дальнейшем планируется переделать данную функцию, с учетом привязки поля модели товара "скидки"

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <новая_цена>, <объект_GoodsDB_№2>: <новая_цена>,... }
    """
    result = {}
    for good in goods:
        result[good] = new_price(good.price, get_promo(good))
    return result


def photo_list(goods):
    """
    функция получения первой фотографии для каждого объекта из для списка товаров из GoodsDB

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <первое_фото_GoodsDB_№1>, <объект_GoodsDB_№2>: <первое_фото_GoodsDB_№2>,... }
    """
    show_photo = {}
    for good in goods:
        show_photo[good] = good.images_for_goods.first()
    return show_photo


def brand_by_count():
    """
    функция получение списка производителей + количества товаров, относящихся к этому производителю

    принимает: ---

    возвращает: словарь вида
    {<объект_BrandNameDB_№1>: int<количество_товаров_GoodsDB_относящихся к нему>,
    <объект_BrandNameDB_№2>: int<количество_товаров_GoodsDB_относящихся к нему>,... }
    """
    all_brands = BrandNameDB.objects.all()
    show_brands = {}
    for item in all_brands:
        show_brands[item] = GoodsDB.objects.filter(brand=item).filter(presence=True).count()
    return show_brands


def category_by_count():
    """
    функция получение списка категорий + количества товаров, относящихся к этой категории

    принимает: ---

    возвращает: словарь вида
    {<объект_CategoryDB_№1>: int<количество_товаров_GoodsDB_относящихся к нему>,
    <объект_CategoryDB_№2>: int<количество_товаров_GoodsDB_относящихся к нему>,... }
    """
    category = CategoryDB.objects.all()
    show_category = {}
    for value in category:
        show_category[value] = GoodsDB.objects.filter(category=value).filter(presence=True).count()
    result = (category, show_category,)
    return result


def get_promo(good):
    """
    Функция получения информации о скидках на данный товар

    принимает: 1 объект GoodsDB

    возвращает: float(значение)
    """
    promo = promo_all.filter(is_active=True).filter(Q(category=good.category) | Q(brand=good.brand))
    discount = list()
    if promo:
        for obj in promo:
            discount.append(obj.discount)
        result = 1 - max(discount)
    else:
        result = 1
    return result


def promo_list(goods):
    """
    функция получения <int_значения> скидки для каждого объекта из для списка товаров из GoodsDB

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <int(1-100)_значение_для_GoodsDB_№1>, <объект_GoodsDB_№2>: <int(1-100)_значение_для_GoodsDB_№2>,... }
    """
    result = {}
    for good in goods:
        result[good] = int((1 - get_promo(good)) * 100)
    return result


def sort_base_funk(goods_dict, rev=True):
    """
    Базовая функция сортировки

    получает: словарь типа
    {<объект_GoodsDB_№1>: <int(1-100)_значение_для_GoodsDB_№1>, <объект_GoodsDB_№2>: <int(1-100)_значение_для_GoodsDB_№2>,... }
    вторым аргументом - булевое значение реверса сортировки, по умолчанию =True

    возвращает: <QuerySet[отсортированный список]>
    """
    result = list(dict(sorted(goods_dict.items(), key=lambda x: x[1], reverse=rev)).keys())
    pk_list = [x.pk for x in result]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
    queryset = GoodsDB.objects.filter(pk__in=pk_list).order_by(preserved).select_related('category').select_related('brand')
    return queryset


def sort_on_rating(goods):
    """
    функция получения списка товаров из GoodsDB, отсортированных по рейтингу + параметру наличия в магазине

    принимает: список объектов из GoodsDB

    возвращает: отсортированный список товаров
    """
    rating_dict = rating_list(goods)
    return sort_base_funk(rating_dict)


def sort_on_price(goods):
    """
    функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
    по возрастанию + параметру наличия в магазине

    принимает: список объектов из GoodsDB

    возвращает: отсортированный список товаров по цене по возрастанию
    """
    price_dict = new_price_list(goods)
    return sort_base_funk(price_dict, False)


def sort_on_price_desc(goods):
    """
    функция получения списка товаров из GoodsDB, отсортированных по цене с учетом скидок,
    по убыванию + параметру наличия в магазине

    принимает: список объектов из GoodsDB

    возвращает: отсортированный список товаров по цене по убыванию
    """
    price_dict = new_price_list(goods)
    return sort_base_funk(price_dict)

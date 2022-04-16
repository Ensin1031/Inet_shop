from django.db.models import Q, Case, When

from .models import *
from main_app.models import *


rating_all = ReviewsDB.objects.select_related('good')
promo_all = PromotionDB.objects.all()


def rating_good(good):
    """
    final rating for one good
    функция высчитывает среднее значение рейтинга для ОДНОГО товара

    принимает: 1 объект товара из GoodsDB

    возвращает: int(значение)
    """
    pre_rating = rating_all.filter(good=good).select_related('good')
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
    return int(old_price * discount)


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
    # promo = PromotionDB.objects.all()
    # print(promo)
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
    queryset = GoodsDB.objects.filter(pk__in=pk_list).order_by(preserved)
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

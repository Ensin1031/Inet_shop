from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *


def rating_good(good):
    '''
    final rating for one good
    функция высчитывает среднее значение рейтинга для ОДНОГО товара

    принимает: 1 объект товара из GoodsDB

    возвращает: int(значение)
    '''
    pre_rating = ReviewsDB.objects.filter(good=good)
    len_rating = len(pre_rating)

    if len_rating > 0:
        sum_rating = 0
        for value in pre_rating:
            sum_rating += int(value.review_rating)
        result = int(sum_rating / len_rating)
        rating = result
    else:
        rating = 0

    return rating


def new_price(old_price):
    """
    функция высчитывает новыю цену за товар, на данный момент условная скидка - 25%.
    В дальнейшем планируется переделать данную функцию, с учетом привязки поля модели товара "скидки"

    принимает: int(значение)

    возвращает: int(значение)
    """
    return int(old_price * 0.75)


def rating_list(good_list):
    '''
    функция высчитывает среднее значение рейтингов для списка товаров

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <среднее_значение_рейтинга>,<объект_GoodsDB_№2>: <среднее_значение_рейтинга>,... }
    '''
    rating = {}
    for obj in good_list:
        rating[obj] = rating_good(obj)
    return rating


def new_price_list(goods):
    '''
    функция высчитывает новую цену для списка товаров из GoodsDB
    В дальнейшем планируется переделать данную функцию, с учетом привязки поля модели товара "скидки"

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <новая_цена>, <объект_GoodsDB_№2>: <новая_цена>,... }
    '''
    result = {}
    for value in goods:
        result[value] = new_price(value.price)
    return result

def photo_list(goods):
    '''
    функция получения первой фотографии для каждого объекта из для списка товаров из GoodsDB

    принимает: список объектов из GoodsDB

    возвращает: словарь вида
    {<объект_GoodsDB_№1>: <первое_фото_GoodsDB_№1>, <объект_GoodsDB_№2>: <первое_фото_GoodsDB_№2>,... }
    '''
    show_photo = {}
    for good in goods:
        show_photo[good] = good.images_for_goods.first()
    return show_photo


def brand_by_count():
    '''
    функция получение списка производителей + количества товаров, относящихся к этому производителю

    принимает: ---

    возвращает: словарь вида
    {<объект_BrandNameDB_№1>: int<количество_товаров_GoodsDB_относящихся к нему>,
    <объект_BrandNameDB_№2>: int<количество_товаров_GoodsDB_относящихся к нему>,... }
    '''
    all_brands = BrandNameDB.objects.all()
    show_brands = {}
    for item in all_brands:
        show_brands[item] = GoodsDB.objects.filter(brand=item).count()
    return show_brands


def category_by_count():
    '''
    функция получение списка категорий + количества товаров, относящихся к этой категории

    принимает: ---

    возвращает: словарь вида
    {<объект_CategoryDB_№1>: int<количество_товаров_GoodsDB_относящихся к нему>,
    <объект_CategoryDB_№2>: int<количество_товаров_GoodsDB_относящихся к нему>,... }
    '''
    category = CategoryDB.objects.all()
    show_category = {}
    for value in category:
        show_category[value] = GoodsDB.objects.filter(category=value).filter(presence=True).count()
    return (category, show_category,)


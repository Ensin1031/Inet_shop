from django.shortcuts import render

from .models import CategoryDB, BrandNameDB, GoodsDB


def category(request):
    """тестовая функция отображения страницы категорий и производителей"""
    categories = CategoryDB.objects.all()
    brands = BrandNameDB.objects.all()
    goods = GoodsDB.objects.all()
    context = {
        'title': 'Категории товаров',
        'categories': categories,
        'brands': brands,
        'goods': goods,
    }
    return render(request, "shopping/category.html", context=context)


def shopping(request):
    '''тестовая функция обработки покупки заказа'''
    return render(request, 'shopping/shopping.html', {'hello': 'Hello, shop!'})


def get_category(request, slug):
    '''тестовая функция просмотра товара по категориям'''
    goods = GoodsDB.objects.filter(category__slug=slug)
    categories = CategoryDB.objects.get(slug=slug)
    context = {
        'title': categories.title,
        'goods': goods,
        'category': categories
    }
    return render(request, 'shopping/get_category.html', context=context)


def show_image(request, slug):
    '''тестовая функция просмотра картинки'''
    return render(request, 'shopping/show_image.html', {'hello': f'Hello, image {slug}!'})


def get_brand(request, slug):
    '''тестовая функция просмотра товара по производителю'''
    goods = GoodsDB.objects.filter(brand__slug=slug)
    brands = BrandNameDB.objects.get(slug=slug)
    context = {
        'title': brands.title,
        'goods': goods,
        'category': brands
    }
    return render(request, 'shopping/brand.html', context=context)


def show_good(request, slug):
    '''тестовая функция просмотра товара по производителю'''
    return render(request, 'shopping/good.html', {'hello': f'Hello, good {slug}!'})

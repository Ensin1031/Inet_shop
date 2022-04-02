from django.shortcuts import render


def index(request):
    '''тестовая функция главной страницы'''
    return render(request, 'main_app/index.html', {'hello': 'Hello, main!'})

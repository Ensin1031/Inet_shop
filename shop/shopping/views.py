from django.shortcuts import render

def shopping(request):
    '''тестовая функция обработки покупки заказа'''
    return render(request, 'shopping/shopping.html', {'hello': 'Hello, shop!'})

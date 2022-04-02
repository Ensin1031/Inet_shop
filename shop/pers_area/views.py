from django.shortcuts import render

def get_lk(request):
    '''функция тестового вывода страницы личного кабинета клиента'''
    return render(request, 'pers_area/pers_area.html', {'hello': 'Hello, pers_area!'})
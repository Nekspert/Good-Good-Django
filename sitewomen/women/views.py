from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import redirect, reverse, render
from django.urls import Resolver404
from django.utils import timezone

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):
    data = {
        'title': 'Главная страница?',
        'menu': menu,
        'float': 28.56,
        'lst': [1, 2, 'abc', True],
        'set': {1, 1, 2, 3, 2, 5},
        'dict': {'key_1': 'value_1', 'key_2': 'value_2'},
        'obj': MyClass(10, 20),
    }

    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest):
    return render(request, 'women/about.html')


def categories_by_id(request: HttpRequest, cat_id: int):
    return HttpResponse(f'<h1>This is the categories by id page with cat_id: {cat_id}.</h1>')


def categories_by_slug(request: HttpRequest, cat_slug: str):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1>This is the categories by slug page with cat_slug: {cat_slug}.</h1>')


def archive(request: HttpRequest, year: int):
    if year > int(timezone.now().year):
        uri = reverse('categories_by_id', args=('123',))
        return redirect(uri, permanent=True)
    return HttpResponse(f'<h1>Archive by years: year: {year}</h1>')


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')

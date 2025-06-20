from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import redirect, reverse, render
from django.urls import Resolver404
from django.utils import timezone

menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
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

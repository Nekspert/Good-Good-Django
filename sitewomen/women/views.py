from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from django.urls import Resolver404

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

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


def show_post(request: HttpRequest, post_id: int):
    return HttpResponse(f'Displaying page with post_id = {post_id}')


def addpage(request):
    return HttpResponse('Add article')


def contact(request):
    return HttpResponse('Feedback')


def login(request):
    return HttpResponse('Authorization')


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')

from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import Resolver404

from .models import Category, Women


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request: HttpRequest):
    posts = Women.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts
    }

    return render(request, 'women/index.html', context=data)


def about(request: HttpRequest):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def show_post(request: HttpRequest, post_slug: str):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'women/post.html', context=data)


def addpage(request: HttpRequest):
    return HttpResponse('Add article')


def contact(request: HttpRequest):
    return HttpResponse('Feedback')


def login(request: HttpRequest):
    return HttpResponse('Authorization')


def show_category(request: HttpRequest, cat_slug: str):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }

    return render(request, 'women/index.html', context=data)


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')

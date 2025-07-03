from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import Resolver404

from .forms import AddPostForm, UploadFileForm
from .models import Category, TagPost, Women


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


def index(request: HttpRequest):
    posts = Women.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }

    return render(request, 'women/index.html', context=data)


def handle_upload_file(f):
    with open(f'uploads/{f.name}', mode='wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request: HttpRequest):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'women/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


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
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # try:
            #     Women.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except django.db.utils.IntegrityError:
            #     form.add_error(None, 'Ошибка добавления поста')
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    data = {
        'menu': menu,
        'title': 'Добавление статьи',
        'form': form
    }
    return render(request, 'women/addpage.html', data)


def contact(request: HttpRequest):
    return HttpResponse('Feedback')


def login(request: HttpRequest):
    return HttpResponse('Authorization')


def show_category(request: HttpRequest, cat_slug: str):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk
    }

    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request: HttpRequest, tag_slug: str):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')

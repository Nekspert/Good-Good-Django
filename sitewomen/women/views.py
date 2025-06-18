from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.urls import Resolver404
from django.utils import timezone


def index(request: HttpRequest):
    return HttpResponse('This is the main page.')


def categories_by_id(request: HttpRequest, cat_id: int):
    return HttpResponse(f'<h1>This is the categories by id page with cat_id: {cat_id}.</h1>')


def categories_by_slug(request: HttpRequest, cat_slug: str):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1>This is the categories by slug page with cat_slug: {cat_slug}.</h1>')


def archive(request: HttpRequest, year: int):
    if year > int(timezone.now().year):
        raise Http404()
    return HttpResponse(f'<h1>Archive by years: year: {year}</h1>')


def page_not_found(request: HttpRequest, exception: Resolver404):
    return HttpResponseNotFound('<h1>Page not found</h1>')

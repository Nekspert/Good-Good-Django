from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest):
    return HttpResponse('This is the main page.')


def categories_by_id(request: HttpRequest, cat_id: int):
    return HttpResponse(f'<h1>This is the categories by id page with cat_id: {cat_id}.</h1>')


def categories_by_slug(request: HttpRequest, cat_slug: str):
    return HttpResponse(f'<h1>This is the categories by slug page with cat_slug: {cat_slug}.</h1>')


def archive(request: HttpRequest, year: int):
    return HttpResponse(f'<h1>Archive by years: year: {year}</h1>')

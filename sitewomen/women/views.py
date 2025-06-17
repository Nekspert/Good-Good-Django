from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest):
    return HttpResponse('This is the main page.')


def categories(request: HttpRequest):
    return HttpResponse('<h1>This is the categories page.</h1>')

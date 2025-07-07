from django.http import HttpRequest, HttpResponse


def login_user(request: HttpRequest):
    return HttpResponse('<h1>login</h1>')


def logout_user(request: HttpRequest):
    return HttpResponse('<h1>logout/h1>')

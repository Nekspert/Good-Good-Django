from django.http import HttpRequest

from women.utils import menu


def get_women_context(request: HttpRequest):
    return {'mainmenu': menu}

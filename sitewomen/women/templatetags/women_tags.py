from django import template

import women.views as views
from women.models import Category


register = template.Library()


@register.inclusion_tag(filename='women/list_categories.html')
def show_categories(cats_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cats_selected': cats_selected}

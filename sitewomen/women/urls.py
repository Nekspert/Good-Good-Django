from django.urls import path, re_path, register_converter

from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cats/<int:cat_id>/', views.categories_by_id, name='categories_by_id'),
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name='categories_by_slug'),
    # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
    path('archive/<year4:year>/', views.archive, name='archive'),
]

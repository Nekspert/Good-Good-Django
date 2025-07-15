from django.urls import path

from . import views

# register_converter(converters.FourDigitYearConverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('deletepage/<slug:post_slug>', views.DeletePage.as_view(), name='delete_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.WomenTagList.as_view(), name='tag'),
    path('edit/<slug:post_slug>/', views.UpdatePage.as_view(), name='edit-page')
]
# re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'),
# path('archive/<year4:year>/', views.archive, name='archive'),

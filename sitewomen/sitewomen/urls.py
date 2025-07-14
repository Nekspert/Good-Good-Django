"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from women.views import page_not_found
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('social-auth/', include('social_django.urls', namespace='social'))
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

handler404 = page_not_found
admin.site.site_header = 'Django [Nekspert] administration'
admin.site.index_title = 'World famous women'

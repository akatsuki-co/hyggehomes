from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from .settings import DEBUG
from .views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home')
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

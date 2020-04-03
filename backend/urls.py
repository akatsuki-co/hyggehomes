from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path

from .settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),

    path('rooms/', include(
        ('stays.urls', 'stay'),
        namespace='stays')
         ),
]

if DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

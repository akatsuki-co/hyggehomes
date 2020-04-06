from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path

from .views import explore_page, landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('explore/', explore_page, name='explore'),
    path('', landing_page, name='landing'),
    path('stays/', include(
        ('apps.stays.urls', 'stay'),
        namespace='stays')
         ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

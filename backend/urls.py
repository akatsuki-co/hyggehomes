from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import path

from .views import landing_page, StayCityListView, ExploreView
from apps.accounts.views import register_view, login_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('', landing_page, name='landing'),
    path('places/<city>', StayCityListView.as_view(), name='places'),
    path('stays/', include(
        ('apps.stays.urls', 'stays'),
        namespace='stays')
         ),
    path('s/', include(
        ('apps.search.urls', 'search'),
        namespace='search')
         ),
    path('user/', include(
        ('apps.accounts.urls', 'user'),
        namespace='user')
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

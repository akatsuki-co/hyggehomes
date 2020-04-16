from django.urls import path

from .views import (
    SearchStaysListView,
)

urlpatterns = [
    path('', SearchStaysListView.as_view(), name='query'),
]

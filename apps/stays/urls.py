from django.urls import path

from apps.stays.views import (
    StayListView,
    StayDetailView,
)

urlpatterns = [
    path('', StayListView.as_view(), name='list'),
    path('<uuid:stay_id>', StayDetailView.as_view(), name='stay_detail'),
]

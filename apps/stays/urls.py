from django.urls import path

from apps.stays.views import (
    StayDetailView,
    make_reservation
)

urlpatterns = [
    path('<id>', StayDetailView.as_view(), name='stay_detail'),
    path('success/', make_reservation, name='success')
]

from django.urls import path

from apps.stays.views import (
    StayDetailView,
    reservation_success
)

urlpatterns = [
    path('<id>', StayDetailView.as_view(), name='stay_detail'),
    path('success/', reservation_success, name='success')
]

from django.urls import path

from apps.stays.views import (
    StayDetailView,
)

urlpatterns = [
    path('<id>', StayDetailView.as_view(), name='stay_detail'),
]

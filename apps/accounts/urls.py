from django.urls import path

from apps.accounts.views import (
    TripsView
)

urlpatterns = [
    path('<id>/trips', TripsView.as_view(), name='trips'),
]

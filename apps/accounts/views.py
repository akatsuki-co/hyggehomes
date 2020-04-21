from django.views.generic import ListView

from apps.stays.models import Stay


class TripsView(ListView):
    """View for Showing all User trips"""
    queryset = Stay.objects.all()
    template_name = 'my_trips.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        print(self.request.user)
        trips = Stay.objects.filter(bookings__guest=self.request.user)
        context['trips'] = trips
        return context

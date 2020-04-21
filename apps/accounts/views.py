from django.views.generic import ListView

from apps.stays.models import Stay


class TripsView(ListView):
    """View for Showing all User trips"""
    queryset = Stay.objects.all()
    template_name = 'my_trips.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        qs = Stay.objects.all().prefetch_related('reviews')
        context['sf_stays_list'] = qs.filter(city="San Francisco")[:4]
        context['featured_stays_list'] = qs.filter(featured=True)[:4]
        return context


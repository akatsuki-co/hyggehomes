from django.shortcuts import render
from django.views.generic import ListView

from apps.stays.models import Stay


def explore_page(request):
    return render(request, 'explore.html')


def landing_page(request):
    return render(request, 'landing.html')


class StayCityListView(ListView):
    """Stay for each City List View"""
    queryset = Stay.objects.all()
    context_object_name = 'stays_list'
    template_name = 'city.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        city = self.kwargs['city']
        context['stays_list'] = Stay.objects.all().filter(city=city)
        context['city'] = city
        return context

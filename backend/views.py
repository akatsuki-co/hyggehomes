from django.shortcuts import render
from django.views.generic import ListView

from apps.stays.models import Stay


class ExploreView(ListView):
    """Several Lists of Stay Views"""
    queryset = Stay.objects.all()
    template_name = 'explore.html'
    explore_cities = [
        {'Paris': 'https://unsplash.com/photos/milUxSbp4_A'},
        {'New York': 'https://unsplash.com/photos/5r5554u-mHo'},
        {'Sydney': 'https://unsplash.com/photos/qaNcz43MeY8'},
        {'Cape Town': 'https://unsplash.com/photos/hzR9rDXWbqo'},
        {'Tokyo': 'https://unsplash.com/photos/alY6_OpdwRQ'},
    ]

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        explore_cities = self.explore_cities
        qs = Stay.objects.all()
        context['explore_cities'] = explore_cities
        context['sf_stays_list'] = qs.filter(city="San Francisco")[:4]
        context['featured_stays_list'] = qs.filter(featured=True)[:4]
        return context


def landing_page(request):
    return render(request, 'landing.html')


class StayCityListView(ListView):
    """Stay for each City List View"""
    queryset = Stay.objects.all()
    template_name = 'city.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        city = self.kwargs['city']
        context['stays_list'] = Stay.objects.all().filter(city=city)
        context['city'] = city
        return context

from django.views.generic import ListView

from apps.stays.models import Stay


class SearchStaysListView(ListView):
    """Search Query of Stays"""
    queryset = Stay.objects.all()
    template_name = 'city.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        request = self.request
        query = request.GET.get('q')
        context['stays_list'] = Stay.objects.all().filter(city=query)
        context['city'] = query
        return context

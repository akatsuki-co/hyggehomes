from django.views.generic import DetailView
from django.http import Http404

from .models import Stay


class StayDetailView(DetailView):
    """Stay Detil View"""
    queryset = Stay.objects.all()
    template_name = 'stays/detail.html'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('id')
        instance = Stay.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Stay doesn't exist")
        return instance

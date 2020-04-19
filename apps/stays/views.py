from django.views.generic import DetailView
from django.http import Http404
from django.shortcuts import render

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


def reservation_success(request):
    if request.method == 'POST':
        user = request.user
        start = request.POST.get('start')
        end = request.POST.get('end')
        guests = request.POST.get('guests')
        print(user)
        stay = request.POST.get('stay')
    return render(request, 'stays/reserved.html')

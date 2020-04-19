from django.views.generic import DetailView
from django.http import Http404
from django.shortcuts import render
from datetime import datetime

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


def make_reservation(request):
    if request.method == 'POST':
        user = request.user
        start = request.POST.get('start')
        end = request.POST.get('end')
        guests = request.POST.get('guests')
        stay_id = request.POST.get('stay')
        if start:
            start = datetime.strptime(start, '%m/%d/%Y').date()
        else:
            raise Http404('Start date must not be None')
        if end:
            end = datetime.strptime(end, '%m/%d/%Y').date()
        else:
            raise Http404('End date must not be None')
        stay = Stay.objects.filter(id=stay_id)\
            .prefetch_related('bookings').first()
        stay.reserve_stay(user, start, end, guests)
    return render(request, 'stays/reserved.html')

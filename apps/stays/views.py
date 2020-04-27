from django.conf import settings
from django.views.generic import DetailView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime

from .models import Stay

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

    def post(self, request, *args, **kwargs):
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
            days = end - start
            booking = stay.reserve_stay(user, start, end, guests)
            if booking:
                charge_price = stay.price * 100 * days.days
                stripe.Charge.create(
                    amount=int(charge_price),
                    currency='usd',
                    description=f'Stay at {stay.title} by {user}',
                    source=request.POST['stripeToken']
                )
            else:
                raise ValueError('Something went wrong...')
            return redirect(
                reverse('user:trips', kwargs={"id": request.user.id})
            )

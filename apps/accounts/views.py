from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.views.generic import ListView

from apps.stays.models import Stay
from apps.bookings.models import Booking

User = get_user_model()


def register_view(request):
    """docstring for register_view"""
    if request.method == "POST":
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if password1 and password2 and password1 == password2:
            new_user, created = User.objects.get_or_create(
                email=email, password=password1)
            if created:
                new_user.set_password(password2)
                new_user.save()
                login(request, new_user)
            else:
                messages.error(request, 'User with email already exists')
            return redirect('explore')
        else:
            messages.error(request, 'Invalid Password')
    else:
        return render(request, 'accounts/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('/explore/')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return redirect('landing')


class TripsView(ListView):
    """View for Showing all User trips"""
    queryset = Stay.objects.all()
    template_name = 'accounts/my_trips.html'

    def get_context_data(self, *args, **kwargs):
        """Method for getting context data"""
        context = super().get_context_data(**kwargs)
        trips = Stay.objects.all().filter(bookings__guest=self.request.user)\
            .active().prefetch_related('bookings')
        context['trips'] = trips
        return context

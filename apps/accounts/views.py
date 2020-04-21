from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import CreateView, FormView, ListView
from django.shortcuts import redirect

from apps.stays.models import Stay
from .forms import RegisterForm, LoginForm

User = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/explore/'


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)
        user = authenticate(email=email, password=password)
        if user is not None:
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
        print(self.request.user)
        trips = Stay.objects.filter(bookings__guest=self.request.user)
        context['trips'] = trips
        return context

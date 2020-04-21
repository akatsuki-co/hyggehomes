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


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/explore/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """Method to check if form is valid"""
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        print("User Authenticated!")
        if user:
            login(request, user)
            print('Logged In!')
            return redirect('/explore/')
        return super(LoginView, self).form_invalid(form)


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

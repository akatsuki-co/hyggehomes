from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Guest


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Guest
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Guest
        fields = ('email',)

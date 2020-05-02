from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class GuestAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('first_name', 'email', 'staff', 'active',)
    list_filter = ('email', 'staff', 'active',)
    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'user_profile',
            'first_name',
            'last_name'
        )}),
        ('Permissions', {'fields': ('staff', 'active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'staff',
                'active'
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, GuestAdmin)

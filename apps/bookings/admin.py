from django.contrib import admin
from .models import Booking

admin.site.register(Booking)


class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_date', 'end_date']

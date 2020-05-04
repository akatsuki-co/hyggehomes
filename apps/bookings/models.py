from django.db import models
from django.conf import settings
import uuid


class BookingManager(models.Manager):
    """Model Manager for Booking a Stay"""
    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(
                user=user, email=user.email)
        return obj, created


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    number_of_guests = models.IntegerField(default=1)
    start_date = models.DateField(u'Start date', help_text=u'Start date')
    end_date = models.DateField(u'End date', help_text=u'End date')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = u'Booking'
        verbose_name_plural = u'Booking'

    def check_overlap(self, new_start, new_end):
        overlap = False
        if (new_start >= self.start_date and new_start <= self.end_date) or\
           (new_end >= self.start_date and new_end <= self.end_date):
            overlap = True
        elif new_start <= self.start_date and new_end >= self.end_date:
            overlap = True
        return overlap

    def __str__(self):
        return f'{self.user.first_name}: {self.start_date} - {self.end_date}'

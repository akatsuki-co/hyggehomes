from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.stays.models import Stay


class Booking(models.Model):
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    stay = models.ForeignKey(Stay, on_delete=models.PROTECT)
    start_date = models.DateField(u'Start date', help_text=u'Start date')
    end_date = models.DateField(u'End date', help_text=u'End date')

    class Meta:
        verbose_name = u'Booking'
        verbose_name_plural = u'Booking'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or\
             (new_end >= fixed_start and new_end <= fixed_end):
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:
            overlap = True

        return overlap

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError('Ending date must after start date')

        bookings = Booking.objects.filter(stay=self.stay)
        if bookings.exists():
            for booking in bookings:
                if self.check_overlap(booking.start_date, booking.end_date,
                                      self.start_date, self.end_date):
                    raise ValidationError(
                        'There is an overlap with another booking by '
                        + str(booking.guest.first_name) + ', ' + str(
                            booking.start_date) + '-' + str(booking.end_date))

    def __str__(self):
        return f'{self.guest.first_name}: {self.start_date} - {self.end_date}'

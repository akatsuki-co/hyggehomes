from django.db import models
from django.urls import reverse
import datetime
import uuid
import os


from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.amenities.models import Amenity
from apps.reviews.models import Review


def get_filename_ext(filepath):
    """Parses the filename for its extension

    Arguments:
        filepath {path} -- filepath of the image uploaded

    Returns:
        name -- name of the image file
        ext -- type of extension of the file
    """
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    """Creates the path for the new uploaded image

    Arguments:
        instance {file} -- instance of the uploaded file
        filename {path} -- path of the instance file

    Returns:
        path -- path of the uploaded image file
    """
    new_filename = instance.title.replace(' ', '_').lower()
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'{final_filename}'


class StayQuerySet(models.query.QuerySet):
    def active(self):
        """docstring for is_active"""
        return self.filter(active=True)

    def featured(self):
        """docstring for featured"""
        return self.filter(featured=True)

    def search(self, query):
        """docstring for search"""
        return self.filter(city=query).distinct()


class StayManager(models.Manager):
    def get_queryset(self):
        """docstring for get_queryset"""
        return StayQuerySet(self.model, using=self._db)

    def all(self):
        """docstring for all """
        return self.get_queryset().active()

    def featured(self):
        """docstring for featured"""
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        return qs.first() if qs.count() == 1 else None

    def by_city(self, city):
        queryset = self.get_queryset().filter(city=city)
        return queryset

    def search(self, query, start, end):
        """docstring for search"""
        queryset = self.get_queryset().active().filter(city=query)
        if not isinstance(start, datetime.date)\
                or not isinstance(end, datetime.date):
            print('Not equal')
            return queryset
        search_results = []
        qs = queryset.prefetch_related('bookings')
        if qs:
            for stay in qs:
                available = True
                for booking in stay.bookings.all():
                    if booking.check_overlap(start, end):
                        available = False
                if available:
                    search_results.append(stay)
        return search_results


class Stay(models.Model):
    """The Stay model

    Arguments:
        models {Model} -- Django builtin Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    host = models.ForeignKey(User, on_delete=models.PROTECT)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    guests = models.IntegerField(default=1)
    bedroom = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    baths = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    plus = models.BooleanField(default=False)
    entire_home = models.BooleanField(default=False)
    check_in = models.CharField(max_length=30)
    description = models.CharField(max_length=1250)
    amenities = models.ManyToManyField(Amenity)
    reviews = models.ManyToManyField(Review, blank=True)
    bookings = models.ManyToManyField(Booking, blank=True)
    featured = models.BooleanField(default=False)
    main_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    second_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    third_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = StayManager()

    def get_absolute_url(self):
        """docstring for get_absolute_url"""
        return reverse("stays:stay_detail", kwargs={"id": self.id})

    def __str__(self):
        """docstring for __str__"""
        return (f'{self.title} - {self.city}')

    def __unicode__(self):
        """docstring for __unicode__"""
        return self.title

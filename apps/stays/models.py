from django.db import models
from django.db.models import Prefetch
from django.urls import reverse
import datetime
import uuid
import os
from statistics import mean

from apps.accounts.models import User
from apps.bookings.models import Booking
from apps.amenities.models import Amenity
from apps.reviews.models import Review

HOME_TYPES = (
    ('Entire place', 'Entire place'),
    ('Private room', 'Private room'),
    ('Shared room', 'Shared room'),
)
CHECK_IN_TYPES = (
    ('Keypad', 'Keypad'),
    ('Lockbox', 'Lockbox'),
    ('Smartlock', 'Smartlock')
)


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
        lookups = (
        )
        return self.filter(lookups).distinct()


class StayManager(models.Manager):
    def get_queryset(self):
        """docstring for get_queryset"""
        return StayQuerySet(self.model, using=self._db)

    def all(self):
        """docstring for all"""
        return self.get_queryset().active()

    def featured(self):
        """docstring for featured"""
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id).prefetch_related(
            Prefetch('amenities')).prefetch_related(Prefetch(
                "reviews",
                queryset=Review.objects.select_related("user")
            ))
        return qs.first()

    def by_city(self, city):
        queryset = self.get_queryset().filter(city=city)
        return queryset

    def search(self, query, start, end, guests):
        """docstring for search"""
        queryset = self.get_queryset().active().filter(city__iexact=query)
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
                if available and stay.guests >= int(guests):
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
    home_types = models.CharField(
        max_length=30, choices=HOME_TYPES, default='Entire place')
    check_in = models.CharField(
        max_length=30, choices=CHECK_IN_TYPES, default='Lockbox')
    description = models.CharField(max_length=1250)
    amenities = models.ManyToManyField(Amenity)
    reviews = models.ManyToManyField(Review, blank=True)
    bookings = models.ManyToManyField(Booking, blank=True)
    featured = models.BooleanField(default=False)
    main_image = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = StayManager()

    def get_absolute_url(self):
        """docstring for get_absolute_url"""
        return reverse("stays:stay_detail", kwargs={"id": self.id})

    def ratings(self):
        """Calculates average ratings for each Stay instance"""
        reviews = self.reviews.all()
        ratings = [review.rating for review in reviews]
        location = [review.location for review in reviews]
        cleanliness = [review.cleanliness for review in reviews]
        hospitality = [review.hospitality for review in reviews]
        average_rating = mean(ratings)
        number_of_reviews = len(reviews)
        average_location = mean(location)
        average_cleanliness = mean(cleanliness)
        average_hospitality = mean(hospitality)
        review_ratings = {
            "average_rating": average_rating,
            "number_of_reviews": number_of_reviews,
            "average_location": average_location,
            "average_cleanliness": average_cleanliness,
            "average_hospitality": average_hospitality
        }
        return review_ratings

    def reserve_stay(self, user, start_date, end_date, guests):
        """Reserve a Stay"""
        if not[x for x in (user, start_date, end_date, guests) if x is None]:
            for booking in self.bookings.all():
                if booking.check_overlap(start_date, end_date):
                    # raise ValueError('Stay is unavailable during these dates')
                    return False
            self.bookings.create(user=user, start_date=start_date,
                                 end_date=end_date, number_of_guests=guests)
            return True
        else:
            raise ValueError("Booking must have a start/end date")

    def __str__(self):
        """docstring for __str__"""
        return (f'{self.title} - {self.city}')

    def __unicode__(self):
        """docstring for __unicode__"""
        return self.title

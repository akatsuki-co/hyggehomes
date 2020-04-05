from django.db import models
from django.db.models import Q
import os

from accounts.models import User


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
    print(final_filename)
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
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(country__icontains=query)
        )
        return self.filter(lookups).distinct()


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

    def search(self, query):
        """docstring for search"""
        return self.get_queryset().active().search(query)


class Stay(models.Model):
    """The Stay model

    Arguments:
        models {Model} -- Django builtin Model
    """
    title = models.CharField(max_length=30)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1250)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    main_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    second_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    third_image = models.ImageField(
        upload_to=upload_image_path, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = StayManager()

    # def get_absolute_url(self):
    #     """docstring for get_absolute_url"""
    #     # return f'/products/{self.slug}/'
    #     return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        """docstring for __str__"""
        return self.title

    def __unicode__(self):
        """docstring for __unicode__"""
        return self.title

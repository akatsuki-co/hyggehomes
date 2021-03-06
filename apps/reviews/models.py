from django.db import models
from django.conf import settings
import uuid

from apps.accounts.models import User


class Review(models.Model):
    """The Review model is for user reviews on each Trail.

    Arguments:
        models {Model} -- Django builtin Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.CharField(max_length=1250)
    rating = models.IntegerField(default=5, blank=True, null=True)
    location = models.IntegerField(default=5, blank=True, null=True)
    cleanliness = models.IntegerField(default=5, blank=True, null=True)
    hospitality = models.IntegerField(default=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at) + ' ' + self.user.first_name

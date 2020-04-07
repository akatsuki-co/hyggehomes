from django.db import models
from django.conf import settings
import uuid

from apps.stays.models import Stay


class Review(models.Model):
    """The Review model is for user reviews on each Trail.

    Arguments:
        models {Model} -- Django builtin Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.CharField(max_length=30)
    body = models.CharField(max_length=1250)
    stars = models.IntegerField(default=5, blank=True, null=True)
    location = models.IntegerField(default=5, blank=True, null=True)
    cleanliness = models.IntegerField(default=5, blank=True, null=True)
    hospitality = models.IntegerField(default=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    Stay = models.ForeignKey(Stay, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject

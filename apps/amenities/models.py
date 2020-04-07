from django.db import models
import uuid


class Amenity(models.Model):
    """The Amenity model is an Amenity for each Stay

    Arguments:
        models {Model} -- Django builtin Model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

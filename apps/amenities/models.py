from django.db import models


class Amenity(models.Model):
    """The Amenity model is an Amenity for each Stay

    Arguments:
        models {Model} -- Django builtin Model
    """
    name = models.CharField(max_length=30)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


from django.db import models
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
    print(name)
    print(ext)
    return name, ext


def upload_image_path(instance, filename):
    """Creates the path for the new uploaded image

    Arguments:
        instance {file} -- instance of the uploaded file
        filename {path} -- path of the instance file

    Returns:
        path -- path of the uploaded image file
    """
    new_filename = instance.name.replace(' ', '_').lower()
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    print(final_filename)
    return f'{final_filename}'


class Stays(models.Model):
    """The Stay model

    Arguments:
        models {Model} -- Django builtin Model
    """
    title = models.CharField(max_length=30)
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=1250)
    main_image = models.ImageField(upload_to='images')
    second_image = models.ImageField(upload_to='images')
    third_image = models.ImageField(upload_to='images')
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

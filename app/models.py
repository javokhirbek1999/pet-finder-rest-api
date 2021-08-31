from django.db import models
from django.utils.translation import gettext as _

from profiles.models import Profile

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

def upload_to(instance, filename):
    return "pets/{filename}".format(filename=filename)

class Pet(models.Model):

    PETS = [
        ("Dog","Dog"),
        ("Cat","Cat"),
        ("Bird","Bird"),
        ("Rabbits","Rabbits"),
        ("Hourses","Hourses"),
        ("Small and Fury Pets","Small and Fury Pets")
    ]
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pet_picture = models.ImageField(_("Pet picture"),upload_to=upload_to, default='pets/default.jpg')
    species = models.CharField(_("Species"),max_length=200, choices=PETS)
    age = models.IntegerField(_("Age"))


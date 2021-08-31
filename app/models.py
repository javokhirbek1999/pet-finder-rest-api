import datetime
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
    title = models.CharField(_("Title"), max_length=200, default="")
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pet_picture = models.ImageField(_("Pet picture"),upload_to=upload_to, default='pets/default.jpg')
    slug = models.SlugField(_("Slug"),max_length=200, unique_for_date='posted',default="")
    posted = models.DateTimeField(_('Posted date'), auto_now_add=True)
    species = models.CharField(_("Species"),max_length=200, choices=PETS)
    age = models.IntegerField(_("Age"))    
    
    @property
    def pet_category(self):
        return self.category.name
    
    @property
    def pet_owner(self):
        return self.owner.user.username

    def __str__(self):
        return self.title
    


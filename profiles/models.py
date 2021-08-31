from django.db import models
from django.utils.translation import gettext as _ 

from authentication.models import User 

def upload_to(instance,filename):
    return "profile/{filename}".format(filename=filename)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(_("Profile picture"), upload_to=upload_to, default='profile/default')
    address = models.CharField(_("Address"), max_length=200)
    city = models.CharField(_("City"), max_length=200)
    country = models.CharField(_("Country"), max_length=200)
    phone = models.CharField(_("Contact number"), max_length=200)

    def __str__(self):
        return self.user.username

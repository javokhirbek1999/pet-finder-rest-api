from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _

from rest_framework_simplejwt.tokens import RefreshToken

class UserManger(BaseUserManager):
    
    def create_user(self, email, username, name, password=None, **other_fields):

        if not email:
            raise ValueError(_('Email is required'))
        
        user = self.model(email=self.normalize_email(email), username=username, name=name)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, name, password):

        user = self.create_user(email=email, username=username, name=name, password=password)

        user.is_superuser = True
        user.is_verified = True
        user.is_active = True
        user.is_staff = True

        user.save(using=self._db)

        return user     

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=250)
    joined_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManger()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username','name')

    def __str__(self):
        return self.username   
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

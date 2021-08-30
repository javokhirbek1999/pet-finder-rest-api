from django.contrib import admin

from .models import User
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email','username','name')
    list_filter = ('email','username','name','is_active','is_staff','is_verified')
    ordering = ('-joined_on',)
    list_display = ('email','id','username','name','is_active','is_staff','is_superuser','is_verified','joined_on','updated_on')
    fieldsets = (
        (None, {'fields': ('email','username')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_superuser','is_active','is_staff','is_verified')}),
    )
    formfield_overrides = {
        models.TextField: {'widget':Textarea(attrs={'rows':20, 'cols':60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','name','password1','password2','is_superuser','is_staff','is_active','is_verified')
        }),
    ) 


admin.site.register(User, UserAdminConfig)
    

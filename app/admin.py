from django.contrib import admin

from .models import Pet, Category

admin.site.register(Category)
admin.site.register(Pet)
from django.contrib import admin

from .models import Pet, Category, Species

@admin.register(Pet)
class AdminPet(admin.ModelAdmin):
    list_display = ('title','id','category','owner','title','age','species','posted')
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category)
admin.site.register(Species)
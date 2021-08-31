from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ('id','pet_category','title','pet_owner','pet_picture','species','age','posted','slug')
    
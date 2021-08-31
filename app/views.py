from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import PetSerializer
from .models import Pet

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Pet.objects.all()

    def get_object(self, **kwargs):
        return Pet.objects.get(slug=self.kwargs.get('pk'))

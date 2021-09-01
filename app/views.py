from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import PetSerializer
from .models import Pet
from .permissions import IsOwner

class BaseClass(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = (IsOwner,)

    def get_object(self, **kwargs):
        return Pet.objects.get(slug=self.kwargs.get('pk'))


class PetViewSet(BaseClass):
    queryset = Pet.objects.all()


class DogsOnly(BaseClass):
    queryset = Pet.objects.filter(category__name="Dogs")


class CatsOnly(BaseClass):
    queryset = Pet.objects.filter(category__name="Cats")


class HoursesOnly(BaseClass):
    queryset = Pet.objects.filter(category__name="Hourses")


class BirdsOnly(BaseClass):
    queryset = Pet.objects.filter(category__name="Birds")


class FuriesOnly(BaseClass):
    queryset = Pet.objects.filter(category__name="Fury")

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from .serializers import ProfileSerializer
from .models import Profile
from .permissions import IsReadOnly


class ProfileView(ModelViewSet):
    permission_classes = (IsReadOnly,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self, **kwargs):
        return Profile.objects.get(user__username=self.kwargs.get('pk'))

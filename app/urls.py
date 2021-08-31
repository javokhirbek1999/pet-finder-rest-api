from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PetViewSet

app_name = 'pets'

router = DefaultRouter()
router.register('pets',PetViewSet, basename='pets')

urlpatterns = [
    path('', include(router.urls)),
]
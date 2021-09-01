from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PetViewSet, DogsOnly, CatsOnly, HoursesOnly, BirdsOnly, FuriesOnly

app_name = 'pets'

router = DefaultRouter()
router.register('pets',PetViewSet, basename='pets')
router.register('dogs', DogsOnly, basename='dogs')
router.register('cats', CatsOnly, basename='cats')
router.register('hourses', HoursesOnly, basename='hourses')
router.register('birds', BirdsOnly, basename='birds')
router.register('fury', FuriesOnly, basename='fury')

urlpatterns = [
    path('', include(router.urls)),
]
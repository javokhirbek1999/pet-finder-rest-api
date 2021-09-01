from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ProfileView

app_name = 'profiles'

router = DefaultRouter()
router.register('',ProfileView,basename='profiles')


urlpatterns = [
    path('', include(router.urls)),
]
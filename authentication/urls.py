from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import RegisterUser, VerifyEmail, LoginAPIView,RegisterSuperuser

app_name = 'authentication'

router = DefaultRouter()
router.register('users', RegisterUser, basename='users')
router.register('admins', RegisterSuperuser, basename='admins')

urlpatterns = [
    path('', include(router.urls)),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
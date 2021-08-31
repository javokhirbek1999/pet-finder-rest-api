import jwt
from django.http import request
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import views, generics, status, viewsets, permissions
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from . import serializers
from .utils import Util


class RegisterSuperuser(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.SuperuserSerializer
    queryset = models.User.objects.filter(is_superuser=True)

    def get_object(self, **kwargs):
        return models.User.objects.get(username=self.kwargs.get('pk'))


class RegisterUser(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = models.User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('authentication:email_verify')
        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)
        email_body = f"Hello {user.name}! Please use the link below to activate your account\n{absurl}"
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify Your Email'}

        Util.send_mail(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

    def get_object(self, **kwargs):
        user_id = self.kwargs['pk']
        return self.queryset.get(username=user_id)


class VerifyEmail(views.APIView):

    serializer_class = serializers.UserSerializer
    
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = models.User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({'status':'Email is successfully verified'},status=status.HTTP_200_OK)
            else:    
                return Response({'status':'Email is already verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'status':'Your token is expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'status':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
            

class LoginAPIView(generics.GenericAPIView):

    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
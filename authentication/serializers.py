from django.db import models
from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from . models import User


class SuperuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username','name','password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                },
            },
        }

    def create(self, validated_data):
        instance = User.objects.create_superuser(**validated_data)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'name', 'password','is_superuser')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type':'password',
                },
            },
            'is_superuser': {
                'read_only': True,
            },
        }
    
    def create(self, validated_data):
        password = self.validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class EmailVerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('token',)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80, min_length=3)
    password = serializers.CharField(max_length=80, min_length=8, write_only=True, style={'input_type':'password'})
    username = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ('email','password','username','tokens')

    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(_('Invalid credentials, try again'))
        
        if not user.is_active:
            raise AuthenticationFailed(_('This user is blocked, please contact the admin'))
        
        if not user.is_verified:
            raise AuthenticationFailed(_('Email is not verified'))

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
        }    

        return super().validate(attrs)

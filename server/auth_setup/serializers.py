from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# import re

#user creating serializer include with validation
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):#validation of Passwod
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user

    def validate_email(self, value):#vaidation of email use to exclude dupilcates
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value


#User listing Serializer with out using password
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]


#token Serializer 
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_admin'] = user.is_superuser
        token['id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['is_active'] = user.is_active
        
        return token   

#password reset serializer
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


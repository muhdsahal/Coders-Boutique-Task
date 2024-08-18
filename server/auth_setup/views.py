from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from .serializers import UserSerializer ,UserListSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView 
from .models import SecurityToken
from .serializers import TokenObtainPairSerializer,PasswordResetSerializer
import secrets
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from django.contrib.auth.hashers import make_password


#User Signup view
class UserSignUpView(APIView):
    def post(self,request,*args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User Created Successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#User Login View 
class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


#User Reset Password View
class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_urlsafe()
            expires_at = timezone.now() + timedelta(hours=1)  

            SecurityToken.objects.create(user=user, token=token, expires_at=expires_at)

            reset_link = f"http://127.0.0.1:8000/api/user/reset-password/?token={token}"
            send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,  
            [email],    
            fail_silently=False,
            )

            return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Confirm Password View 
class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.query_params.get('token')
        new_password = request.data.get('new_password')
        print(token, new_password, "two")
        if not token or not new_password:
            return Response({'detail': 'Token and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset_token = SecurityToken.objects.get(token=token)
            if reset_token.expires_at < timezone.now():
                return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)

            user = reset_token.user
            user.set_password(new_password)
            user.save()

            reset_token.delete()

            return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)

        except SecurityToken.DoesNotExist:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        

#User ForgotPassword View 
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            token = secrets.token_urlsafe()
            expires_at = timezone.now() + timedelta(hours=1)  

            SecurityToken.objects.create(user=user, token=token, expires_at=expires_at)

            reset_link = f"http://127.0.0.1:8000/api/user/confirm-password/{token}/"
            send_mail(
            'Password Reset Request',
            f'Click the following link to reset your password: {reset_link}',
            settings.DEFAULT_FROM_EMAIL,  
            [email],    
            fail_silently=False,
            )

            return Response({'detail': 'Password reset email sent.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Confirm Pass word View
class ResetPasswordView(APIView):
    def post(self, request, token):
        try:
            reset_token = SecurityToken.objects.get(token=token)
            print(reset_token,'reset tokennrerfefefe',token)
        except SecurityToken.DoesNotExist:
            return Response({'detail': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password and confirm_password:
            check  = reset_token.is_expired()
            print(check, "check logging")
            if  reset_token.is_expired():
                return Response({'detail': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)


            if new_password != confirm_password:
                return Response({'detail': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

            user = reset_token.user
            user.password = make_password(new_password)
            user.save()

            reset_token.delete()

            return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({"details" : "confirm password is required"}, status=status.HTTP_400_BAD_REQUEST)
        

#Pagination View setuped 5 content in 1 page
class Setpagination(PageNumberPagination):
    page_size = 5

# List all the users 
class ListUsersView(ListAPIView): 
    permission_classes = [IsAuthenticated,IsAdminUser] # only can access this API For Admins
    pagination_class = Setpagination #Pagination
    queryset = User.objects.all() 
    serializer_class = UserListSerializer 

# This API Used for user get by id(get,put,delete)
class ListUserById(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,IsAdminUser] # only can access this API for Admins
    queryset = User.objects.all()
    serializer_class = UserListSerializer
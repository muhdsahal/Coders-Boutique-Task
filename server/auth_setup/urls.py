from django.urls import path
from .views import( UserSignUpView ,TokenObtainPairView,PasswordResetView,
                PasswordResetConfirmView,ForgotPasswordView,ResetPasswordView,ListUsersView,ListUserById)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/',UserSignUpView.as_view(),name='signup'),#user signup
    path('token/',TokenObtainPairView.as_view(),name='token'),#user login
    path('token/refresh/',TokenRefreshView.as_view(),name='token-refresh'),# token refresh
    path('user/password-reset/', PasswordResetView.as_view(), name='password-reset-request'), # reset password
    path('user/reset-password/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'), #reset confirm password
    path('user/forgot-password/',ForgotPasswordView.as_view(),name='forgot-passowrd'), #forgot password
    path('user/confirm-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'), # forgot confirm password
    path('list_users/', ListUsersView.as_view(), name='list-users'), # list all the users
    path('list_user/<int:pk>/', ListUserById.as_view(), name='list-users-byid'),#retrive,update ,delete by user

    



]


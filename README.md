
---

### Project Overview:

A project for social networking application using django restframework

### What I Did:
 
### How I Made It Happen:

- **Technology Used:**
- I used Django and Django REST Framework.
- MYSQL as database
- JWT for Authentication
  
- **Testing and Notes:**
   - Checked everything was working using a tool called Postman.
   - Wrote down all the steps in a document so others can understand and use it later.


Installation process 



---

## Project Structure

The project is structured as follows:

- `server/` - Project folder
- `auth_setup/` - Django app for management


## Setup Instructions

### 1. Create Virtual Environment

```
    python -m venv myvenv
```

### 2. Activate Virtual Environment

```
    venv\scripts\activate
```

### 3. Install Dependencies

Install required packages using pip:

```
    pip install django djangorestframework rest_framework-simplejwt mysqlclient
```

### 4. Create Django Project and App

```
    django-admin startproject server
    django-admin startapp auth_setup
```

### 5. Configuration

#### Update `settings.py`

Add the following apps to `INSTALLED_APPS` in `server/settings.py`:

```
    INSTALLED_APPS = [
        # ...
      'auth_setup',
      'rest_framework',
      'rest_framework_simplejwt',
      
        # ...
    ]
```

### 6. rest_framework Configuration
```
REST_FRAMEWORK = {

        'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ],
 
    'DEFAULT_AUTHENTICATION_CLASSES': (
    
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),

    
}
```
### 6. URL Configuration
```

from django.urls import path,include
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


```

### 7. Database Setup

Run Django migrations to set up the database:

```
    python manage.py makemigrations
    python manage.py migrate
```


### 8. Run Development Server

Start the development server:

```
    python manage.py runserver
```




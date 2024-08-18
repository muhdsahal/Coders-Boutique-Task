from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SecurityToken(models.Model):#This model for reset password and change password
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
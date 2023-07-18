from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class CustomUser(AbstractUser):
    pass
    is_client = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    currency = models.CharField(max_length=3, default="USD")


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile")

    money_in_wallet = models.IntegerField(default=0)

    is_client = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        if self.is_client:
            user_type = "client"
        elif self.is_vendor:
            user_type = "vendor"
        elif self.is_moderator:
            user_type = "moderator"
        else:
            user_type = "undefined"
        return f"{self.user.username} - {user_type}"


class VendorProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="vendor_profile")


class ModeratorProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="moderator_profile")


class ClientProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="client_profile")

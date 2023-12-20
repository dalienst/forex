import base64
import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from accounts.abstracts import UniversalIdModel, TimeStampedModel
from cloudinary.models import CloudinaryField


from forexapp.settings.base import AUTH_USER_MODEL


class User(AbstractUser, UniversalIdModel, TimeStampedModel):
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def get_full_name(self) -> str:
        return super().get_full_name()
    
    def get_short_name(self) -> str:
        return super().get_short_name()
    
    def get_username(self) -> str:
        return super().get_username()
    


class Client(TimeStampedModel):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="client",
    )
    image = CloudinaryField("client_images", blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    identification = models.BigIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username


class Admin(TimeStampedModel):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="admin",
    )
    image = CloudinaryField("admin_image", blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username



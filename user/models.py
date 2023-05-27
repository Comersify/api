from django.db import models
from django.contrib.auth.models import AbstractUser
import os


def make_profile_image_path(instance, filename):
    username = instance.username
    filename = f"profile_{filename}"
    return os.path.join(f'uploads/{instance.type}', username, filename)


def make_logo_image_path(instance, filename):
    username = instance.user.username
    filename = f"logo_{filename}"
    return os.path.join('uploads/vendors', username, filename)


def make_cover_image_path(instance, filename):
    username = instance.user.username
    filename = f"cover_{filename}"
    return os.path.join('uploads/vendors', username, filename)


class CustomUser(AbstractUser):

    class TypeChoices(models.TextChoices):
        ADMIN = "ADMIN", "ADMIN"
        VENDOR = "VENDOR", "VENDOR"
        CUSTOMER = "CUSTOMER", "CUSTOMER"

    phone_number = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to=make_profile_image_path, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, default="sad")
    last_name = models.CharField(max_length=20, default="sam")
    username = models.CharField(max_length=20, unique=True)
    user_type = models.CharField(
        choices=TypeChoices.choices, default=TypeChoices.CUSTOMER, max_length=10)
    REQUIRED_FIELDS = ['email', 'first_name',
                       'last_name']

    def save(self, *args, **kwargs):
        self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)


class ShippingInfo(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)


class Store(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to=make_logo_image_path)
    cover = models.ImageField(upload_to=make_cover_image_path)

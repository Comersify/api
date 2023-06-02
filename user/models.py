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
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(upload_to="uplaods/user", null=True, blank=True)
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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={
        'user__user_type': 'VENDOR'})
    name = models.CharField(max_length=30)
    description = models.TextField()
    logo = models.ImageField(
        upload_to=make_logo_image_path, null=True, blank=True)
    cover = models.ImageField(
        upload_to=make_cover_image_path, null=True, blank=True)


class AppReviews(models.Model):
    class IntegerChoices(models.IntegerChoices):
        CHOICE_ONE = 1, 'One'
        CHOICE_TWO = 2, 'Two'
        CHOICE_THREE = 3, 'Three'
        CHOICE_FOUR = 4, 'Four'
        CHOICE_FIVE = 5, 'Five'

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    stars = models.IntegerField(choices=IntegerChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

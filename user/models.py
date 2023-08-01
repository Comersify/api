from django.db import models
from django.contrib.auth.models import AbstractUser
from cryptography.fernet import Fernet
import os
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4
from django.conf import settings
from errors import NotValidUser


def make_profile_image_path(instance, filename):
    username = instance.username
    filename = f"profile_{filename}"
    return os.path.join(f'uploads/{instance.user_type}', username, filename)


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
        INDIVIDUAL_SELLER = "INDIVIDUAL-SELLER", "INDIVIDUAL-SELLER"
        STORE_OWNER = "STORE-OWNER", "STORE-OWNER"

    phone_number = models.CharField(max_length=15, blank=True)
    image = models.ImageField(
        upload_to=make_profile_image_path, null=True, default="media/avatar.jpeg")
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, default="sad")
    last_name = models.CharField(max_length=20, default="sam")
    username = models.CharField(max_length=30, unique=True)
    user_type = models.CharField(
        choices=TypeChoices.choices, default=TypeChoices.CUSTOMER, max_length=30)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to=make_profile_image_path, null=True, blank=True)
    REQUIRED_FIELDS = ['email', 'first_name',
                       'last_name']

    def save(self, *args, **kwargs):
        self.username = self.email.split("@")[0]
        super().save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)
        response_data = {
            "type": "success",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'exp': refresh.payload['exp'],
            "name": self.first_name,
            "image": self.image.url
        }
        return response_data


class Token(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        is_not_individual_vendor = self.user.user_type != "INDIVIDUAL-SELLER"
        is_not_store_owner = self.user.user_type != "STORE-OWNER"
        if is_not_individual_vendor and is_not_store_owner:
            raise NotValidUser("User can't create token")
        key = Fernet.generate_key()
        fernet = Fernet(key)
        user_id = uuid4().__str__() + str(self.user.id)
        encrypted_token = fernet.encrypt(user_id.encode()).decode()
        self.token = encrypted_token
        super().save(*args, **kwargs)


class ShippingInfo(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, limit_choices_to={
                             "user_type": "customer"}, null=True)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=20)


class Store(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={
        'user_type': 'VENDOR'})
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

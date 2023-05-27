from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class WhiteList(models.Model):

    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    products = models.ManyToManyField("product.Product")

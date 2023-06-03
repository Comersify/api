from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class WishList(models.Model):

    user = models.OneToOneField(USER, on_delete=models.CASCADE, limit_choices_to={
                                'user_type': 'CUSTOMER'})
    products = models.ManyToManyField("product.Product")

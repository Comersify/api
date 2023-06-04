from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class ShoppingCart(models.Model):

    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,  limit_choices_to={
        'user_type': 'CUSTOMER'})
    orders = models.ManyToManyField("order.Order",  limit_choices_to={
        'status': 'IN_CART'})

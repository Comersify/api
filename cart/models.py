from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class ShoppingCart(models.Model):

    class StatusChoices(models.TextChoices):

        SUBMITTED = "SUBMITTED", "SUBMITTED"
        IN_PROGRESSE = "IN_PROGRESSE", "IN_PROGRESSE"

    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True,  limit_choices_to={
        'user__user_type': 'CUSTOMER'})
    orders = models.ManyToManyField("order.Order",  limit_choices_to={
        'order__status': 'IN_CART'})

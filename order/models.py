from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        IN_CART = 'IN_CART', "IN_CART"
        SUBMITTED = 'SUBMITTED', "SUBMITTED"
        SHIPPED = 'SHIPPED', "SHIPPED"
        DELEVRED = 'DELEVRED', "DELEVRED"

    user = models.ForeignKey(USER, on_delete=models.CASCADE, limit_choices_to={
        'user__user_type': 'CUSTOMER'})
    product = models.ForeignKey(
        "product.Product", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.IN_CART, max_length=10)

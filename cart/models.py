from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class ShoppingCart(models.Model):

    class StatusChoices(models.TextChoices):

        SUBMITTED = "SUBMITTED", "SUBMITTED"
        IN_PROGRESSE = "IN_PROGRESSE", "IN_PROGRESSE"

    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    orders = models.ManyToManyField("order.Order")
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.IN_PROGRESSE)

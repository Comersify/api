from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date
USER = get_user_model()


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        IN_CART = 'IN_CART', "IN_CART"
        SUBMITTED = 'SUBMITTED', "SUBMITTED"
        SHIPPED = 'SHIPPED', "SHIPPED"
        DELEVRED = 'DELEVRED', "DELEVRED"

    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, limit_choices_to={
        'user_type': 'CUSTOMER'})
    product = models.ForeignKey(
        "product.Product", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    pack = models.ForeignKey('product.ProductPackage',
                             on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.IN_CART, max_length=10)
    coupon = models.ForeignKey(
        "product.Coupon", on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"product": models.F('product'), "end_date__lt": date.today()})
    price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    def clean(self) -> None:
        if self.product.id and self.pack.product.id != self.product.id:
            raise ValidationError("Pack is not valid")
        if self.product.id and self.coupon.product.id != self.product.id:
            raise ValidationError("Coupon is not valid")
        return super().clean()

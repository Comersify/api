from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

USER = get_user_model()


class Order(models.Model):

    class StatusChoices(models.TextChoices):
        IN_CART = 'IN_CART', "IN_CART"
        SUBMITTED = 'SUBMITTED', "SUBMITTED"
        SHIPPED = 'SHIPPED', "SHIPPED"
        DELEVRED = 'DELEVRED', "DELEVRED"

    user = models.ForeignKey(USER, on_delete=models.CASCADE, limit_choices_to={
        'user_type': 'CUSTOMER'}, null=True)
    shipping_info = models.ForeignKey(
        'user.ShippingInfo', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    pack = models.ForeignKey('product.ProductPackage',
                             on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        choices=StatusChoices.choices, default=StatusChoices.IN_CART, max_length=10)
    coupon = models.ForeignKey(
        "product.Coupon", on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"product": models.F('product')})
    price = models.FloatField(null=True, blank=True)
    shipping = models.ForeignKey(
        'product.shipping', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if self.product.id and self.pack.product.id != self.product.id:
            raise ValidationError("Pack is not valid")
        if self.coupon and self.coupon.end_date > timezone.now():
            if self.product.id and self.coupon.product.id != self.product.id:
                raise ValidationError("Coupon is not valid")
        if not self.user and self.product.user.user_type != "INDIVIDUAL-SELLER":
            raise ValidationError("User not valid")
        self.price = self.product.current_price * self.quantity + self.shipping.price
        if self.coupon:
            self.price -= self.coupon.value
        return super().save(*args, **kwargs)

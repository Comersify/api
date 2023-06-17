from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import os

USER = get_user_model()


def make_product_image_path(instance, filename):
    username = instance.product.store.user.username
    filename = f"p_{instance.product.id}_{instance.id}.jpeg"
    return os.path.join('./uploads/vendors', username, 'product', filename)


def make_product_packs_image_path(instance, filename):
    username = instance.product.store.user.username
    filename = f"pk_{instance.product.id}_{instance.id}.jpeg"
    return os.path.join('./uploads/vendors', username, 'product', filename)


class Category(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={"parent__isnull": True})
    name = models.CharField(max_length=100)


class Product(models.Model):
    store = models.ForeignKey(
        'user.Store', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.FloatField()
    buy_price = models.FloatField()
    in_stock = models.IntegerField()

    @property
    def current_price(self):
        from datetime import datetime
        discount = Discount.objects.filter(
            end_date__gt=datetime.now(), product_id=self.pk)
        act_price = self.price
        if discount.exists():
            discount = discount.get()
            act_price -= discount.percentage * self.price / 100
        return act_price

    def __str__(self) -> str:
        return self.title


class ProductPackage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=make_product_packs_image_path)
    title = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=make_product_image_path)


class Review(models.Model):
    class IntegerChoices(models.IntegerChoices):
        CHOICE_ONE = 1, 'One'
        CHOICE_TWO = 2, 'Two'
        CHOICE_THREE = 3, 'Three'
        CHOICE_FOUR = 4, 'Four'
        CHOICE_FIVE = 5, 'Five'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True, limit_choices_to={
        'user_type': 'CUSTOMER'})
    review = models.TextField()
    stars = models.IntegerField(choices=IntegerChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)


class Coupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    value = models.FloatField(validators=[
        MinValueValidator(1, message='Minimum value is 1.'),
    ])
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    start_date = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        if self.product and self.product.price < self.value:
            return ValidationError("Value is not valid")
        return super().clean()


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    percentage = models.PositiveIntegerField(validators=[
        MinValueValidator(0, message='Minimum value is 1.'),
        MaxValueValidator(90, message='Maximum value is 100.')
    ])
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    start_date = models.DateTimeField(auto_now_add=True)

from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import os
USER = get_user_model()


def make_product_image_path(instance, filename):
    username = instance.product.user.username
    filename = f"p_{instance.product.id}_{instance.id}.jpeg"
    return os.path.join('./uploads/vendors', username, 'product', filename)


def make_product_packs_image_path(instance, filename):
    username = instance.product.user.username
    filename = f"pk_{instance.product.id}_{instance.id}.jpeg"
    return os.path.join('./uploads/vendors', username, 'product', filename)


class Category(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={"user_type__in":[USER.TypeChoices.INDIVIDUAL_SELLER, USER.TypeChoices.STORE_OWNER]})
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={"parent__isnull": True})
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Packaging(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE)
    packaging = models.ManyToManyField(Packaging)
    related_product = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    price = models.FloatField()
    buy_price = models.FloatField(null=True, blank=True)
    in_stock = models.IntegerField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # SlugField

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def current_price(self):
        discount = Discount.objects.filter(
            end_date__gt=timezone.now(), product_id=self.pk)
        act_price = self.price
        if discount.exists():
            discount = discount.last()
            act_price -= discount.percentage * self.price / 100
        return act_price

    def __str__(self) -> str:
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vendor/product')


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
        MinValueValidator(0.01, message='Minimum value is 0.01.'),
    ])
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    start_date = models.DateTimeField(auto_now_add=True)

    def clean(self) -> None:
        if self.product and self.product.price < self.value:
            return ValidationError("Value is not valid")
        return super().clean()


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discounted_price = models.PositiveIntegerField(validators=[
        MinValueValidator(0.01, message='Minimum value is 1.')
    ])
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    start_date = models.DateTimeField(auto_now_add=True)


class Shipping(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, limit_choices_to={
        'user_type': 'VENDOR'})
    wilaya = models.CharField(max_length=20)
    price = models.FloatField(
        validators=[MinValueValidator(0, "Price Can not be less then 0")])

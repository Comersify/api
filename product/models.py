from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

USER = get_user_model()

class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE)
    name   = models.CharField(max_length=100)

class ProductImage(models.Model):
    image = models.ImageField(upload_to="images/products/")

class Product(models.Model):
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    categoryID = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) 
    description = models.TextField()
    price = models.FloatField()
    images = models.ManyToManyField(ProductImage)

    def __str__(self) -> str:
        return self.title
    
class ProductPackage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/products-package/")
    title = models.CharField(max_length=100)


class Review(models.Model):

    class IntegerChoices(models.IntegerChoices):
        CHOICE_ONE = 1, 'One'
        CHOICE_TWO = 2, 'Two'
        CHOICE_THREE = 3, 'Three'
        CHOICE_FOUR = 4, 'Four'
        CHOICE_FIVE = 5, 'Five'

    
    user = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    stars = models.IntegerField(choices=IntegerChoices.choices)


class Coupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    percentage = models.IntegerField(validators=[
            MinValueValidator(0, message='Minimum value is 1.'),
            MaxValueValidator(90, message='Maximum value is 100.')
        ])
    end_date = models.DateTimeField()
    start_date = models.DateTimeField(auto_now_add=True)


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    percentage = models.IntegerField(validators=[
            MinValueValidator(0, message='Minimum value is 1.'),
            MaxValueValidator(90, message='Maximum value is 100.')
        ])
    end_date = models.DateTimeField()
    start_date = models.DateTimeField(auto_now_add=True)
        
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"user_type__in":[User.TypeChoices.INDIVIDUAL_SELLER, User.TypeChoices.STORE_OWNER]})
    domain = models.CharField(max_length=20, unique=True)
    logo = models.ImageField()
    title = models.CharField(max_length=20)
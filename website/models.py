from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"user_type__in":[User.TypeChoices.INDIVIDUAL_SELLER, User.TypeChoices.STORE_OWNER]})
    domain = models.CharField(max_length=200, unique=True)
    test_domain = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
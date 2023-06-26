from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tracker(models.Model):
    id = models.CharField(primary_key=True, auto_created=True, unique=True, max_length=20)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id} " + f"related to {self.user.get_username()}" if self.user else ""


class Visit(models.Model):
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE)
    client_url = models.CharField(max_length=50)
    api_url = models.CharField(max_length=50)
    browser = models.CharField(max_length=20)
    browser_version = models.CharField(max_length=20)
    ip_address = models.GenericIPAddressField()
    logged_in = models.BooleanField(default=False)

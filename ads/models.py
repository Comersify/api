from django.db import models


class Ads(models.Model):
    image = models.ImageField(upload_to="uploads/ads")
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)

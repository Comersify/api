from django.urls import path
from .views import *

urlpatterns = [
    path("ads/", GetAdsView.as_view())
]

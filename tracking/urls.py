from django.urls import path
from .views import *

urlpatterns = [
    path("init/", CreateTracker.as_view()),
]

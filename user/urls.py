from django.urls import path
from .views import update_account

urlpatterns = [
    path("account/update/", update_account)
]

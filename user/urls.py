from django.urls import path
from .views import *

urlpatterns = [
    path("account/update/", update_account),
    path("login/", login),
    path("signup/", signup),
    path("store/<int:id>", get_store_by_id),
    path("store/top/", top_stores),
    path("app-reviews/", get_app_reviews),
    path("shipping-info/", get_addresse),
    path("shipping-info/create/", create_addresse),
]
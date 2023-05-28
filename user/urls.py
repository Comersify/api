from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("account/update/", update_account),
    path("login/", csrf_exempt(LoginView.as_view())),
    path("signup/", signup),
    path("store/<int:id>", csrf_exempt(GetStoreByIDView.as_view())),
    path("store/top/", top_stores),
    path("app-reviews/", get_app_reviews),
    path("shipping-info/", get_addresse),
    path("shipping-info/create/", create_addresse),
]

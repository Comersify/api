from django.urls import path
from .views import *

urlpatterns = [
    path("account/info/", SettingsView.as_view()),
    path("account/update/", UpdateSettingsView.as_view()),  # ver
    path("login/", LoginView.as_view()),  # ver
    path("refresh/", RefreshTokenView.as_view()),  # ver
    path("signup/", SignupView.as_view()),  # ver
    path("stores/id/<int:id>/", csrf_exempt(GetStoreByIDView.as_view())),
    path("stores/top/", GetTopStorseView.as_view()),  # ver
    path("app-reviews/", get_app_reviews),  # ver
    path("shipping-info/", get_addresse),
    path("shipping-info/create/", create_addresse),
]

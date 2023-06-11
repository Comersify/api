from django.urls import path
from .views import *

urlpatterns = [
    path("account/info/", SettingsView.as_view()),
    path("vendor/customers/", GetCustomersView.as_view()),
    path("account/update/", UpdateSettingsView.as_view()),  # ver
    path("login/", LoginView.as_view()),  # ver
    path("refresh/", RefreshTokenView.as_view()),  # ver
    path("signup/", SignupView.as_view()),  # ver
    path("stores/id/<int:id>/", GetStoreByIDView.as_view()),
    path("stores/top/", GetTopStorseView.as_view()),  # ver
    path("app-reviews/", GetAppReviewsView.as_view()),  # ver
]

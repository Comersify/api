from django.urls import path
from .views import *


urlpatterns = [
    path("my-orders/", GetMyOrdersView.as_view()),  # ver
    path("orders/create/", CreateOrderView.as_view()),
]

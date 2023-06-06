from django.urls import path
from .views import *


urlpatterns = [
    path("my-orders/", GetMyOrdersView.as_view()),  # ver
    path("order/create/", CreateOrderView.as_view()),
]

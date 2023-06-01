from django.urls import path
from .views import *


urlpatterns = [
    path("my-orders/", get_my_orders), # ver
    path("orders/create/", create_order),
]

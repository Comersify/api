from django.urls import path
from .views import *


urlpatterns = [
    path("orders/", get_orders),
    path("orders/create/", create_order),
]

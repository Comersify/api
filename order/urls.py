from django.urls import path
from .views import *


urlpatterns = [
    path("my-orders/", GetMyOrdersView.as_view()),  
    path("order/create/", CreateOrderView.as_view()),
    path("individual-seller/order/create/", CreateOrderForIndividualSeller.as_view()),
    path("vendor/orders/", VendorOrdersView.as_view())
]

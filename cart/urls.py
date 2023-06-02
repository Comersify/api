from django.urls import path
from .views import *

urlpatterns = [  # ver
    path("cart/products/", GetCartDetailsView.as_view()),
    path("cart/add-product/", AddProoductToCartView.as_view()),
    path("cart/delet-product/", DeleteProoductFromCartView.as_view()),
    path("cart/update-product/", UpdateProoductInCartView.as_view()),
]

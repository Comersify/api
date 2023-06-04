from django.urls import path
from .views import *

urlpatterns = [  # ver
    path("cart/products/", GetCartDetailsView.as_view()),
    path("cart/add-product/", AddProoductToCartView.as_view()),
    path("cart/delete-product/", DeleteProoductFromCartView.as_view()),
    path("cart/update-product/", UpdateProoductInCartView.as_view()),
    path("cart/apply-coupon/", ApplyCouponView.as_view()),
]

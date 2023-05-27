from django.urls import path
from .views import *

urlpatterns = [

    path("products/", get_product),
    path("products/create/", create_product),
    path("products/delete/<int:id>/", delete_product),
    path("products/update/<int:id>/", update_product),

    path("coupons/", get_coupon),
    path("coupons/create/", create_coupon),
    path("coupons/delete/<int:id>/", delete_coupon),
    path("coupons/update/<int:id>/", update_coupon),

    path("coupons/", get_discount),
    path("coupons/create/", create_discount),
    path("coupons/delete/<int:id>/", delete_discount),
    path("coupons/update/<int:id>/", update_discount),
]

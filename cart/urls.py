from django.urls import path
from .views import *

urlpatterns = [  # ver
    path("cart/products/", get_cart_details),
    path("cart/add-product/", add_product_to_cart),
    path("cart/delet-product/", delete_product_from_cart),
    path("cart/update-product/", update_product_in_cart),
]

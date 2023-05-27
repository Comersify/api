from django.urls import path
from .views import * 

urlpatterns = [
    path("cart/<int:id>/products/", get_cart_details),
    path("cart/<int:id>/add-product/", add_product_to_cart),
    path("cart/<int:id>/delet-product/", delete_product_from_cart),

]
from django.urls import path
from .views import * 

urlpatterns = [
    path("wish-list/products/", get_wish_list_details),
    path("wish-list/add-product/", add_product_to_wish_list),
    path("wish-list/delete-product/", delete_product_from_wish_list),
]
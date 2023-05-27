from django.urls import path
from .views import * 

urlpatterns = [
    path("wish-list/<int:id>/products/", get_wish_list_details),
    path("wish-list/<int:id>/add-product/", add_product_to_wish_list),
    path("wish-list/<int:id>/delet-product/", delete_product_from_wish_list),
]
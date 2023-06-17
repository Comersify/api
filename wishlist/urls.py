from django.urls import path
from .views import *

urlpatterns = [
    path("wish-list/products/", GetWishListDetailsView.as_view()),
    path("wish-list/has-product/<int:id>", ProductInWishListView.as_view()),
    path("wish-list/add-product/", AddProductToWishListView.as_view()),
    path("wish-list/delete-product/", DeleteProductFromWishList.as_view()),
    path("check/", index),
]

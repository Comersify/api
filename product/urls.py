from django.urls import path
from .views import *

urlpatterns = [

    path("products/", get_product),
    path("my-products/", get_my_product),
    path("products/create/", create_product),
    path("products/delete/<int:id>/", delete_product),
    path("products/update/<int:id>/", update_product),
    path("products/top-deals/", top_deals),
    path("products/<int:id>/", get_product_details),

    path("categories/top/", top_categories),
    path("categories/", get_categories),

    path("product/<int:id>/reviews", get_reviews),

    path("coupons/", get_coupon),
    path("coupons/<int:id>", get_coupon_by_id),
    path("coupons/create/", create_coupon),
    path("coupons/delete/<int:id>/", delete_coupon),
    path("coupons/update/<int:id>/", update_coupon),

    path("discounts/", get_discount),
    path("discounts/create/", create_discount),
    path("discounts/delete/<int:id>/", delete_discount),
    path("discounts/update/<int:id>/", update_discount),
]

from django.urls import path
from .views import *

urlpatterns = [

    path("products/", get_product),
    path("my-products/", get_my_product),
    path("products/create/", create_product),
    path("products/delete/<int:id>/", delete_product),
    path("products/update/<int:id>/", update_product),
    path("products/super-deals/", top_deals), # ver
    path("products/<int:id>/", get_product_details),

    path("categories/top/", top_categories), # ver
    path("categories/", get_categories), # ver

    path("product/<int:id>/reviews", get_reviews), # ver

    path("my-coupons/", get_coupon),
    path("coupon/<str:code>", get_coupon_by_code), # ver
    path("coupons/create/", create_coupon),
    path("coupons/delete/<int:id>/", delete_coupon),
    path("coupons/update/<int:id>/", update_coupon),

    path("discounts/", get_discount),
    path("discounts/create/", create_discount),
    path("discounts/delete/<int:id>/", delete_discount),
    path("discounts/update/<int:id>/", update_discount),
]

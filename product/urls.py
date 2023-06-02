from django.urls import path
from .views import *

urlpatterns = [

    path("products/", GetProductsView.as_view()),
    path("my-products/", GetMyProductsView.as_view()),
    path("products/create/", CreateProductView.as_view()),
    path("products/delete/<int:id>/", DeleteProductView.as_view()),
    path("products/update/<int:id>/", UpdateProductView.as_view()),
    path("products/super-deals/", GetSuperDealsView.as_view()),  # ver
    path("products/<int:id>/", GetProductDetailsView.as_view()),

    path("categories/top/", GetHotCategoriesView.as_view()),  # ver
    path("categories/", GetCategoriesView.as_view()),  # ver

    path("product/<int:id>/reviews", GetReviewsView.as_view()),  # ver

    path("my-coupons/", GetCouponView.as_view()),
    path("coupon/<str:code>", GetCouponByCodeView.as_view()),  # ver
    path("coupons/create/", CreateCouponView.as_view()),
    path("coupons/delete/<int:id>/", DeleteCouponView.as_view()),
    path("coupons/update/<int:id>/", UpdateCouponView.as_view()),

    path("discounts/", GetDiscountView.as_view()),
    path("discounts/create/", CreateDiscountView.as_view()),
    path("discounts/delete/<int:id>/", DeleteCouponView.as_view()),
    path("discounts/update/<int:id>/", UpdateProductView.as_view()),
]

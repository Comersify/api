from django.urls import path
from .views import *

urlpatterns = [

    path("products/", GetProductsView.as_view()),
    path("my-products/", GetMyProductsView.as_view()),
    path("products/super-deals/", GetSuperDealsView.as_view()),  # ver
    path("products/id/<int:id>/", GetProductDetailsView.as_view()),

    path("categories/top/", GetHotCategoriesView.as_view()),  # ver
    path("categories/", GetCategoriesView.as_view()),  # ver

    path("coupon/<str:code>", GetCouponByCodeView.as_view()),  # ver
    path("reviews/<int:id>", GetReviewsView.as_view()),  # ver


    path("vendor/products/", ProductView.as_view()),
    path("vendor/coupons/", CouponView.as_view()),
    path("vendor/discounts/", DiscountView.as_view()),

]

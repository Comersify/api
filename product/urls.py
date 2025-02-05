from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'attributes', AttributeViewSet, basename="attribute")
router.register(r'attribute-values', AttributeValueViewSet, basename="attribute-value")

urlpatterns = [
    # Use the router to handle the following
    path('v2/', include(router.urls)),  # This will automatically handle all viewsets

    # If you still need custom views, define them here
    path("products/super-deals/", GetSuperDealsView.as_view()),  
    path("products/id/<int:id>/", GetProductDetailsView.as_view()),
    path("categories/top/", GetHotCategoriesView.as_view()),  
    path("categories/", CategoriesView.as_view()),  
    path("reviews/<int:id>", GetReviewsView.as_view()),  # Custom view for reviews
    path("dashboard/", DashboardDataView.as_view()),
    path("vendor/products/", ProductView.as_view()),
    path("vendor/products/<int:id>", ProductDetailsView.as_view()),
    path("vendor/coupons/", CouponView.as_view()),
    path("vendor/discounts/", DiscountView.as_view()),
]
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from product.models import Product

class ProductFilter(filters.FilterSet):
    price_gte = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_lte = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category_id', 'price', 'price_gte', 'price_lte']



class ProductPagination(PageNumberPagination):
    page_size = 20               # Default items per page
    page_size_query_param = 'page_size'  # Allow client to override with ?page_size=20
    max_page_size = 100         # Limit max size to avoid abuse
    page_query_param = 'page' 
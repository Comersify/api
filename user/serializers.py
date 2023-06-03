from .models import Store, AppReviews
from django.db.models import Count, Avg, Value
from product.serializers import ProductSerializer
from rest_framework import serializers
from django.db.models.functions import Coalesce


class StoreSerializer:
    def get_top_stores(self):
        stores = Store.objects.annotate(order_count=Count(
            'product__order'), reviews_avg=Avg('product__review')).order_by('-order_count', "-reviews_avg").values('id', 'name', 'logo', 'description', 'reviews_avg')[:8]
        return list(stores)

    def get_store_details(self, id):
        store = Store.objects.filter(pk=id).annotate(
            orders=Count('product__order'),
            reviews=Count('product__review'),
            reviews_avg=Coalesce(Avg('product__review'), Value(0.0))
        )
        if not store.exists():
            return False
        store = store.get()
        products = ProductSerializer().get_products_by_store_id(store_id=id)
        data = {
            "id": store.id,
            "cover": store.cover.url,
            "logo": store.logo.url,
            "name": store.name,
            "description": store.description,
            "orders": store.orders,
            "reviews": store.reviews,
            "reviews_avg": store.reviews_avg,
            "products": products
        }
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppReviews
        fields = '__all__'

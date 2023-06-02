from .models import Store, AppReviews
from django.db.models import Count, Avg
from product.serializers import ProductSerializer
from rest_framework import serializers


class StoreSerializer:
    def get_top_stores(self):
        stores = Store.objects.annotate(order_count=Count(
            'product__order'), reviews_avg=Avg('product__review')).order_by('-order_count', "-reviews_avg").values('name', 'logo', 'description', 'reviews_avg')[:8]
        return list(stores)

    def get_store_details(self, id):
        store = Store.objects.filter(id=id).annotate(
            orders=Count('product__order'),
            reviews=Count('product__review'),
            reviews_avg=Avg('product__review')
        )
        if not store.exists():
            return False
        data = {
            "cover": store.cover.url,
            "logo": store.logo.url,
            "name": store.name,
            "description": store.description,
            "orders": store.orders,
            "reviews": store.reviews,
            "products": ProductSerializer().get_data(store_id=id)
        }
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppReviews
        fields = '__all__'

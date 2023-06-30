from .models import Store, AppReviews
from django.db.models import Count, Sum, Avg, Value, Subquery, OuterRef, Q
from django.contrib.auth import get_user_model
from product.serializers import ProductSerializer
from rest_framework import serializers
from django.db.models.functions import Coalesce
from order.models import Order

USER = get_user_model()


class StoreSerializer:
    def get_top_stores(self):
        subquery_order = Order.objects.filter(status="DELEVRED").filter(
            id=OuterRef('id')).annotate(orders_count=Count('id')).values('orders_count')[:1]
        stores = Store.objects.annotate(order_count=Subquery(subquery_order), reviews_avg=Coalesce(Avg('product__review__stars'), Value(0.0))
                                        ).order_by('-order_count', "-reviews_avg"
                                                   ).values(
            'id', 'name', 'logo', 'order_count',
            'description', 'reviews_avg'
        )[:8]
        return list(stores)

    def get_store_details(self, id):
        subquery_order = Order.objects.filter(product__user__id=OuterRef(
            'id'), status="DELEVRED").annotate(orders_count=Count('id')).values('orders_count')[:1]
        store = Store.objects.filter(pk=id).annotate(
            orders=Coalesce(Subquery(subquery_order), 0),
            reviews=Count('product__review'),
            reviews_avg=Coalesce(Avg('product__review__stars'), Value(0.0))
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


class CustomersSerializer:
    def get_data(self, user_id):
        customers = USER.objects.annotate(
            spent=Sum("order__price", filter=Q(
                order__status="DELEVRED", order__product__user__id=user_id)),
            orders=Count(
                "order", filter=Q(order__status="DELEVRED", order__product__user__id=user_id)),
            reviews=Count("review")
        ).filter(orders__gt=0).values(
            'first_name', 'last_name', 'image',
            'orders', 'reviews', 'spent'
        )
        return customers

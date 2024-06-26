from product.models import ProductImage
from order.models import Order
from django.db.models import OuterRef, Subquery
from .models import Order


class OrderSerializer:
    def get_data(self, user_id):
        subquery_product_image = ProductImage.objects.filter(
            product_id=OuterRef('product_id')).values('image')
        orders = Order.objects.filter(
            product__user__id=user_id
        ).annotate(
            product_image=Subquery(subquery_product_image)
        ).select_related('product', 'coupon').values(
            'id', 'product__title', 'product_image', 'price', 'pack__title', "status", "shipping_info__address", "shipping_info__phone_number", "shipping_info__postal_code",
            'coupon__code', 'created_at', 'user__first_name', 'user__last_name', 'user__image'
        )
        return orders

    def get_orders_for_analytics(self, user_id):
        data = Order.objects.filter(product__user_id=user_id).order_by('created_at').values(
            'id', 'price', 'created_at','shipping__wilaya', 
            'user__first_name', 'user__last_name'
        )
        return list(data)
    

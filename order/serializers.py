from product.models import ProductImage
from order.models import Order
from django.db.models import OuterRef, Subquery
from .models import Order


class OrderSerializer:
    def get_data(self, user_id):
        subquery_product_image = ProductImage.objects.filter(
            product_id=OuterRef('product_id')).values('image')
        orders = Order.objects.filter(
            product__store__user__id=user_id
        ).annotate(
            product_image=Subquery(subquery_product_image)
        ).select_related('product', 'coupon').values(
            'id', 'product__title', 'product_image', 'price', 'pack__title', "status",
            'coupon__code', 'created_at', 'user__first_name', 'user__last_name', 'user__image'
        )
        return orders

from product.models import Discount, ProductImage
from order.models import Order
from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import Coalesce


class DiscountSerializer:
    def get_data(self, user_id):
        order_subquery = Order.objects.filter(
            status="DELEVRED",
            product__user__id=user_id,
            created_at__lt=OuterRef('end_date'),
            created_at__gte=OuterRef('start_date')

        ).annotate(orders=Count('pk')).values('orders')[:1]
        product_image_subquery = ProductImage.objects.filter(
            product_id=OuterRef('product__id')).values('image')[:1]

        discounts = Discount.objects.filter(
            product__user__id=user_id
        ).annotate(
            product_image=Subquery(product_image_subquery),
            orders=Coalesce(Subquery(order_subquery), 0)).values(
            'id', 'title', 'percentage', 'end_date', 'product__title', 'product_image', 'product__id',
        )
        return discounts

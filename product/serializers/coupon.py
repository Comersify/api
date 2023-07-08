from product.models import ProductImage, Coupon
from order.models import Order
from django.db.models import Count, OuterRef, Subquery
from django.contrib.auth import get_user_model


User = get_user_model()


class CouponSerializer:
    def get_data(self, user_id):
        order_subquery = Order.objects.filter(
            status="DELEVRED",
            product__user__id=user_id,
            coupon_id=OuterRef('id')).annotate(orders=Count('pk')).values('orders')[:1]

        product_image_subquery = ProductImage.objects.filter(
            product_id=OuterRef('product__id')).values('image')[:1]

        coupons = Coupon.objects.filter(
            product__user__id=user_id
        ).annotate(
            product_image=Subquery(product_image_subquery),
            orders=Subquery(order_subquery)
        ).select_related('product').values(
            'id', 'code', 'value', 'end_date',
            'product_image', 'product__title', 'product__id',
        )

        return coupons

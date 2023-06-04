from .models import ShoppingCart
from product.models import ProductImage, Discount
from django.db.models import Value, F, Sum, OuterRef, Subquery, ExpressionWrapper
from django.db import models
from decimal import Decimal, ROUND_DOWN
from django.db.models.functions import Coalesce


class ShoppingCartSerializer:
    def get_data(self, id):
        subquery_image = ProductImage.objects.filter(
            product_id=OuterRef('product_id')).values('image')[:1]
        subquery_discount = Discount.objects.filter(
            product_id=OuterRef('product_id')).values('percentage')[:1]
        cart = ShoppingCart.objects.filter(
            user_id=id).get()
        orders = cart.orders.all().prefetch_related(
            'pack', 'product'
        ).annotate(
            product__image=Subquery(subquery_image),
            product__discount=Subquery(subquery_discount),
        ).values(
            'id', 'pack__title', 'product__title',
            'product__id', 'quantity', 'product__price',
            'product__image', 'product__discount'
        )
        coupons = cart.orders.filter(
            coupon__isnull=False).prefetch_related('coupon', 'product').values(
            'coupon__id', 'coupon__code', 'coupon__percentage', 'product__price'
        )
        checkout = cart.orders.all().annotate(
            order_price=ExpressionWrapper(
                (F('quantity') * F('product__price')), output_field=models.FloatField(null=True)),
            discounted_price=ExpressionWrapper(
                F('quantity')*(
                    F('product__discount__percentage') * F('product__price')/100
                ), output_field=models.FloatField(null=True)),
        ).aggregate(
            sub_total=Coalesce(Sum('order_price'), Value(0.0)),
            total_discount=Coalesce(Sum('discounted_price'), Value(0.0)),
        )
        total = checkout['sub_total'] - checkout['total_discount']
        data = {
            "orders": list(orders),
            "coupons": list(coupons),
            "checkout": {
                "sub_total": checkout['sub_total'],
                "discount": checkout['total_discount'],
                "total": total,
            },
        }
        print(data['checkout'])
        return data

from .models import ShoppingCart
from product.models import ProductImage, Discount
from django.db.models import Value, F, Sum, OuterRef, Subquery, ExpressionWrapper
from django.db import models
from django.db.models.functions import Coalesce
from datetime import date


class ShoppingCartSerializer:

    def get_coupons(self, cart):
        coupons = cart.orders.filter(
            coupon__isnull=False
        ).prefetch_related('coupon', 'product').values(
            'coupon__id', 'coupon__code',
            'coupon__value', 'product__price'
        )
        coupons_total = cart.orders.filter(
            coupon__isnull=False
        ).prefetch_related('coupon').aggregate(total=Sum('coupon__value'))

        return coupons, coupons_total

    def get_orders(self, cart):
        subquery_image = ProductImage.objects.filter(
            product_id=OuterRef('product_id')).values('image')[:1]
        subquery_discount = Discount.objects.filter(
            product_id=OuterRef('product_id')).values('percentage')[:1]

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
        return orders

    def get_checkout(self, cart):
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
        return checkout

    def get_data(self, id):
        cart = ShoppingCart.objects.filter(
            user_id=id).get()

        coupons, coupons_total = self.get_coupons(cart)
        orders = self.get_orders(cart)
        checkout = self.get_checkout(cart)
        total = checkout['sub_total'] - checkout['total_discount']

        if coupons_total['total']:
            total -= coupons_total['total']
            print(coupons_total['total'])
        data = {
            "orders": list(orders),
            "coupons": list(coupons),
            "checkout": {
                "sub_total": checkout['sub_total'],
                "discount": checkout['total_discount'],
                "total": total,
            },
        }
        return data

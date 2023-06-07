from .models import WishList
from product.models import ProductImage, Discount, Product
from django.db.models import Count, Value, OuterRef, Subquery, Avg
from django.db.models.functions import Coalesce
from order.models import Order


class WishListSerializer:

    def get_products(self, products):
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_discount = Discount.objects.filter(
            product=OuterRef('id')
        ).order_by("-id").values('percentage')[:1]

        subquery_completed_orders = Order.objects.filter(
            product=OuterRef('id'), status='DELEVRED'
        ).values('product').annotate(count_completed_orders=Count('id')).values('count_completed_orders')[:1]

        products = products.annotate(
            orders=Coalesce(Subquery(subquery_completed_orders), Value(0)),
            discount_value=Coalesce(Subquery(subquery_discount), Value(0)),
            image=Subquery(subquery_image),
            reviews=Coalesce(Avg('review__stars'), Value(0.0))
        )
        products = products.filter(in_stock__gt=0).values(
            'id', 'title', 'price', 'discount_value', 'orders', 'image', 'reviews')
        return products

    def get_data(self, user_id):
        wish_list = WishList.objects.filter(user_id=user_id)
        if not wish_list.exists():
            return []
        wish_list = wish_list.get()
        products = wish_list.products.all()
        products = self.get_products(products)
        return products

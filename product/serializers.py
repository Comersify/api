from .models import Product, Discount, Review, ProductImage, Category
from order.models import Order
from django.db.models import Count, Value, OuterRef, Subquery, Avg, Aggregate
from django.db.models.functions import Coalesce
from django.db import models


class ProductSerializer():

    def get_products(self, has_discount=False):
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_discount = Discount.objects.filter(
            product=OuterRef('id')
        ).values('percentage')[:1]

        subquery_completed_orders = Order.objects.filter(
            product=OuterRef('id'), status='DELEVRED'
        ).values('product').annotate(count_completed_orders=Count('id')).values('count_completed_orders')[:1]

        products = Product.objects.annotate(
            orders=Coalesce(Subquery(subquery_completed_orders), Value(0)),
            discount_value=Coalesce(Subquery(subquery_discount), Value(0)),
            image=Subquery(subquery_image),
            reviews=Coalesce(Avg('review__stars'), Value(0.0))
        )
        if has_discount:
            products = products.filter(discount_value__gt=10)

        products = products.filter(in_stock__gt=0).values(
            'id', 'title', 'price', 'discount_value', 'orders', 'image', 'reviews')
        return products

    def get_super_deals(self):
        products = self.get_products(has_discount=True)
        super_deals = products.order_by('orders')[:8]
        return list(super_deals)

    def get_products_by_store_id(self, store_id):
        products = self.get_products().filter(store_id=store_id)
        return list(products)


class CategorySerializer:

    def get_all_categories(self):
        categories = Category.objects.filter(parent__isnull=True)
        return categories

    def get_hot_categories(self):
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_completed_orders = Order.objects.filter(
            product=OuterRef('id'), status='DELEVRED'
        ).values('product').annotate(count_completed_orders=Count('id')).values('count_completed_orders')[:1]

        subquery_product = Product.objects.annotate(
            image=Subquery(subquery_image),
            orders=Subquery(subquery_completed_orders)
        ).filter(
            categoryID=OuterRef('id')
        ).order_by('-orders').values('id')[:4]

        categories = Category.objects.annotate(
            products=Subquery(subquery_product),
        ).filter(
            parent__isnull=False
        ).values('name', 'products')[:1]
        return list(categories)

    def test(self):
        categories = Category.objects.all()

        results = Product.objects.filter(
            categoryID__in=Subquery(categories.values('pk'))
        ).order_by('categoryID', 'pk').annotate(category_count=Subquery(
            categories.values('pk')
            .annotate(product_count=models.Count('product'))
            .filter(pk=OuterRef('categoryID_id'))
            .values('product_count')
        )).filter(category_count__lte=4)[:4]
        return results

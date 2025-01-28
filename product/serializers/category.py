from product.models import Product, ProductImage, Category
from order.models import Order
from django.db.models import Count, OuterRef, Subquery
from django.db import models


class CategorySerializer:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def get_all_categories(self):
        categories = Category.objects.filter(
            user_id=self.user_id).values('id', 'name', 'parent_id')
        return list(categories)

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
            category=OuterRef('id')
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
        ).order_by('category', 'pk').annotate(category_count=Subquery(
            categories.values('pk')
            .annotate(product_count=models.Count('product'))
            .filter(pk=OuterRef('categoryID_id'))
            .values('product_count')
        )).filter(category_count__lte=4)[:4]
        return results

from .models import Shipping, Product, Discount, ProductImage, Category, ProductPackage, Review
from order.models import Order
from django.db.models import Count, Sum, Value, OuterRef, Subquery, Q, Avg, F, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Coupon


User = get_user_model()


class IndividualSellerProductSerializer:
    def __int__(self, request):
        self.owner = request.owner

    def get_products(self):
        products = Product.objects.filter(user=self.owner)
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_discount = Discount.objects.filter(
            product=OuterRef('id'),
            end_date__gt=timezone.now()
        ).order_by("-id").values('percentage')[:1]

        products = Product.objects.annotate(
            discount_value=Coalesce(Subquery(subquery_discount), Value(0)),
            image=Subquery(subquery_image),
            act_price=ExpressionWrapper(
                F('price')-Coalesce(
                    F('discount_value') * F('price')/100, 0), output_field=models.FloatField()),
        )

        products = products.filter(in_stock__gt=0).values(
            'id', 'title', 'price', 'discount_value',
            'act_price', 'image')
        return products


class ProductSerializer:

    def get_products(self, has_discount=False):
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_discount = Discount.objects.filter(
            product=OuterRef('id'),
            end_date__gt=timezone.now()
        ).order_by("-id").values('percentage')[:1]

        products = Product.objects.annotate(
            orders=Count(
                "order", filter=Q(order__status="DELEVRED")
            ),
            discount_value=Coalesce(Subquery(subquery_discount), Value(0)),
            image=Subquery(subquery_image),
            reviews=Coalesce(Avg('review__stars'), Value(0.0)),
            act_price=ExpressionWrapper(
                F('price')-Coalesce(
                    F('discount_value') * F('price')/100, 0), output_field=models.FloatField()),
        )
        if has_discount:
            products = products.filter(discount_value__gt=10)

        products = products.filter(in_stock__gt=0).values(
            'id', 'title', 'price', 'discount_value',
            'act_price', 'orders', 'image', 'reviews')
        return products

    def get_super_deals(self):
        products = self.get_products(has_discount=True)
        super_deals = products.order_by('orders')[:8]
        return list(super_deals)

    def get_products_by_store_id(self, store_id):
        products = self.get_products().filter(store_id=store_id)
        return list(products)

    def get_product_details(self, id):
        subquery_discount = Discount.objects.filter(
            product=OuterRef('id'),
            end_date__gt=timezone.now()
        ).order_by("-id").values('percentage')[:1]

        products = Product.objects.annotate(
            orders=Count(
                "order", filter=Q(order__status="DELEVRED")
            ),
            discount_value=Coalesce(Subquery(subquery_discount), Value(0)),
            reviews_avg=Coalesce(Avg('review__stars'), Value(0.0)),
            reviews=Coalesce(Count('review__stars'), Value(0)),
        )

        products = products.filter(id=id).values(
            'id', 'title', 'price', 'discount_value', 'orders', 'reviews', 'description', 'reviews_avg'
        ).get()

        products["images"] = ProductImage.objects.filter(
            product_id=id).values('image')

        products["packs"] = list(ProductPackage.objects.filter(
            product_id=id).values('id', 'image', 'title', 'quantity'))

        products["shipping"] = Shipping.objects.filter(
            user_id=Product.objects.filter(
                id=id).get().user.id
        ).values('id', 'wilaya', 'price')
        return products

    def get_products_for_vendor(self, user_id):
        subquery_image = ProductImage.objects.filter(
            product=OuterRef('id')
        ).values('image')[:1]

        subquery_discount = Discount.objects.filter(
            product=OuterRef('id'),
            end_date__gt=timezone.now()
        ).order_by("-id").values('percentage')[:1]

        products = Product.objects.filter(user__id=user_id).annotate(
            image=Subquery(subquery_image),
            packs=Coalesce(Count('productpackage'), 0),
            discount_value=Coalesce(Subquery(subquery_discount), 0),
            orders=Count(
                "order", filter=Q(order__status="DELEVRED")
            ),
            act_price=ExpressionWrapper(
                F('price')-Coalesce(
                    F('discount_value') * F('price')/100, 0),
                output_field=models.FloatField()
            ),
            earning=Coalesce(
                Sum("order__price", filter=Q(order__status="DELEVRED")), 0.0),
            reviews=Coalesce(Count('review__stars'), Value(0)),
            reviews_avg=Coalesce(Avg('review__stars'), Value(0.0)),
        ).values(
            'id', 'image', 'title', 'price', 'buy_price', 'act_price', 'in_stock', 'packs', 'earning',
            'orders', 'reviews', 'reviews_avg',
        )
        return products

    def get_product_details_for_vendor(self, user_id, product_id):
        product = Product.objects.filter(
            user__id=user_id,
            id=product_id
        )
        if not product.exists():
            return False
        product = product.values(
            'id', 'title', 'category__id', 'in_stock', 'price', 'description')
        product_image = ProductImage.objects.filter(product_id=product_id)
        if not product_image.exists():
            return False
        product_image = product_image.values('id', 'image')
        product_package = ProductPackage.objects.filter(product_id=product_id)
        if product_package.exists():
            product_package = product_package.values(
                "id", "image", 'title', 'quantity')
        else:
            product_package = []

        data = [product, list(product_image), list(product_package)]
        return data


class CategorySerializer:

    def get_all_categories(self):
        categories = Category.objects.filter(
            parent__isnull=True).values('id', 'name')
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


class ReviewsSerializer:
    def get_reviews(self, id):
        subquery_user_image = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('image')[:1]

        subquery_user_first_name = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('first_name')[:1]

        subquery_user_last_name = User.objects.filter(
            id=OuterRef('id'),
            user_type='CUSTOMER'
        ).values('last_name')[:1]

        reviews = Review.objects.filter(product_id=id).annotate(
            image=Subquery(subquery_user_image),
            last_name=Subquery(subquery_user_first_name),
            first_name=Subquery(subquery_user_last_name),
        ).values('review', 'stars', 'created_at', 'image', 'last_name', 'first_name')

        return list(reviews)

    def get_reviews_stats(self, id):
        total = Review.objects.filter(product_id=id).count()
        if total == 0:
            return {
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
            }
        percent = 100/total
        stats = {
            1: Review.objects.filter(product_id=id, stars=1).count() * percent,
            2: Review.objects.filter(product_id=id, stars=2).count() * percent,
            3: Review.objects.filter(product_id=id, stars=3).count() * percent,
            4: Review.objects.filter(product_id=id, stars=4).count() * percent,
            5: Review.objects.filter(product_id=id, stars=5).count() * percent
        }
        return stats


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

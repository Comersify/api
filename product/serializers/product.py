from product.models import Shipping, Product, Discount, ProductImage, ProductPackage
from django.db.models import Count, Sum, Value, OuterRef, Subquery, Q, Avg, F, ExpressionWrapper
from django.db.models.functions import Coalesce
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class IndividualSellerProductSerializer:
    def __int__(self, request):
        self.owner = request.owner

    def get_products(self):
        products = Product.objects.filter(user_id=self.owner.id)
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
        from user.models import Store
        store_obj = Store.objects.filter(id=store_id)
        if not store_obj.exists():
            return False
        user_id = store_obj.get().user.id
        products = self.get_products().filter(user_id=user_id)
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

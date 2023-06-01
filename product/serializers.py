from rest_framework import serializers
from .models import Product, Discount, Review, ProductImage
from order.models import Order


class ProductSerializer(serializers.Serializer):

    def get_data(self, store_id=None):
        data = []
        products = None
        if store_id:
            products = Product.objects.filter(store__id=store_id)
        else:
            product = Product.objects.all()
        for product in products:
            product_data = {
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "reviews": Review.objects.filter(product__id=product.id).count(),
                "orders": Order.objects.filter(product__id=product.id, status="DELEVRED").count()
            }
            images = ProductImage.objects.filter(product__id=product.id)
            if len(images) > 1:
                product_data["image"] = images[0].image.url
            else:
                product_data["image"] = images.get().image.url
            discount = Discount.objects.filter(product__id=product.id)
            if discount.exists():
                product_data["discount"] = discount.get().percentage
            data.append(product_data)
        return data

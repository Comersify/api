from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import IndividualSellerProductSerializer, ProductSerializer, CategorySerializer, ReviewsSerializer, CouponSerializer, DiscountSerializer
from django.db.models import Q
from .models import Coupon, Discount, Product, ProductPackage, ProductImage, Review
from rest_framework.permissions import IsAuthenticated
from core.backend import *
from datetime import date
from django.db.models import Sum
import json
from user.models import Store
from order.models import Order
from django.utils import timezone
from permissions import HasOwner

class GetSuperDealsView(APIView):
    def get(self, request):
        try:
            serializer = ProductSerializer()
            data = serializer.get_super_deals()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetHotCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_hot_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetProductsView(APIView):
    permission_classes = [HasOwner]
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        if request.owner == "INDIVIDUAL-SELLER":
            serializer = IndividualSellerProductSerializer(request)
            products = serializer.get_products()
            return Response({"type":"success", "data": products})
        
        serializer = ProductSerializer()
        products = serializer.get_products()
        keyword = request.GET.get('q')
        offset = int(request.GET.get("offset")) if request.GET.get(
            "offset") else False
        price_from = int(request.GET.get('from')) if request.GET.get(
            'from') else False
        price_to = int(request.GET.get('to')) if request.GET.get(
            'to') else False
        stars = int(request.GET.get('stars')) if request.GET.get(
            'stars') else False
        categories = request.GET.get(
            'categories').replace(" ", "").split(",") if request.GET.get(
            'categories') else ['']
        orderby = request.GET.get('orderBy')
        if keyword:
            products = products.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        if price_from != '' and price_from > 0:
            products = products.filter(act_price__gte=price_from)
        if price_to != '' and price_to > 0:
            products = products.filter(act_price__lte=price_to)
        if stars > 0:
            products = products.filter(reviews__gte=stars)
        if categories != ['']:
            categories = [int(cat) for cat in categories]
            products = products.filter(category_id__in=categories)
        if orderby:
            if orderby == "act_price":
                products = products.order_by(orderby)
            else:
                products = products.order_by(f"-{orderby}")

        paginate_from = False
        paginate_to = False
        if offset:
            paginate_to = offset * 10
            paginate_from = paginate_to - 10
            products = products[paginate_from:paginate_to]

        return Response({"type": "success", "data": products[:15]})


class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request, id):
        if request.user.user_type == "VENDOR":
            serializer = ProductSerializer()
            data = serializer.get_product_details_for_vendor(
                request.user.id, id)
            if not data:
                return Response({"type": "error", "message": "Product not found"})
            return Response({"type": "success", "data": data})
        return Response({"type": "error", "message": "user not valid"})


class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        if request.user.user_type == "VENDOR":
            serializer = ProductSerializer()
            data = serializer.get_products_for_vendor(request.user.id)
            if not data:
                return Response({"type": "error", "message": "Product not found"})
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "user not valid"})

    def post(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        data = request.data.get('data')
        if data is None:
            return Response({"type": "error", "message": "Pls complete your product information"})

        data = json.loads(data)
        title = data.get('title')
        category_id = data.get('category')
        price = data.get('price')
        buy_price = data.get('buy_price')
        description = data.get('description')
        quantity = data.get('quantity')

        if not buy_price or not title or not category_id or not price or not description or not quantity:
            return Response({"type": "error", "message": "Pls complete your product information"})
        if not quantity and not request.data.get('pack_quantity[0]') and not request.data.get('title[0]') and not request.data.get('pack[0]'):
            return Response({"type": "error", "message": "Complete needed information"})

        store = Store.objects.filter(user_id=request.user.id)
        if not store.exists():
            return Response({"type": "error", "message": "Can't create product"})
        store = store.get()
        product = Product.objects.create(
            store_id=store.id,
            title=title,
            category_id=category_id,
            price=price,
            buy_price=buy_price,
            description=description,
            in_stock=quantity,
        )

        if request.data.get('image[0]') is None:
            return Response({"type": "error", "message": "Product image is missing"})

        i = 0
        total_quantity = 0
        while True:
            pack_title = request.data.get(f'title[{i}]')
            pack_image = request.data.get(f'pack[{i}]')
            pack_quantity = request.data.get(f'quantity[{i}]')
            if pack_title and pack_image:
                product_pack = ProductPackage.objects.create(
                    product_id=product.id,
                    title=json.loads(pack_title),
                    image=pack_image
                )
                i += 1
                total_quantity += pack_quantity
            else:
                break
        if total_quantity > 0:
            product.in_stock = total_quantity
        for i in range(4):
            product_image = request.data.get(f'image[{i}]')

            if product_image:
                image = ProductImage.objects.create(
                    product_id=product.id,
                    image=product_image
                )
            else:
                break

        return Response({"type": "success", "message": "product created successfully "})

    def delete(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        product_id = request.data.get('id')
        if product_id is None:
            return Response({"type": "error", "message": "data is missing"})
        product = Product.objects.filter(
            user__id=request.user.id, id=product_id
        )
        if not product.exists():
            return Response({"type": "error", "message": "Product not found"})
        product.delete()
        return Response({"type": "success", "message": "Product was deleted"})

    def put(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        data = request.data.get('data')

        if data is None:
            return Response({"type": "error", "message": "data is missing"})

        data = json.loads(data)
        product_id = data.get("id")
        title = data.get("title")
        category = data.get("category")
        description = data.get("description")
        price = data.get("price")
        buy_price = data.get("buy_price")
        quantity = data.get("quantity")
        images = data.get("images")
        packs = data.get("packs")

        if not buy_price or not product_id or not title or not category or not description or not price:
            return Response({"type": "error", "message": "Complete needed information"})
        if not quantity and not request.data.get('pack_quantity[0]') and not request.data.get('title[0]') and not request.data.get('pack[0]'):
            return Response({"type": "error", "message": "Complete needed information"})

        product = Product.objects.filter(
            user__id=request.user.id,
            id=product_id
        )
        if not product.exists():
            return Response({"type": "error", "message": "Product not found"})
        product = product.get()

        deleted_product_images = ProductImage.objects.filter(
            product_id=product.id).exclude(id__in=images)
        deleted_product_packs = ProductPackage.objects.filter(
            product_id=product.id).exclude(id__in=packs)
        deleted_product_images.delete()
        deleted_product_packs.delete()
        i = 0
        total_quantity = 0
        while True:
            pack_title = request.data.get(f'title[{i}]')
            pack_image = request.data.get(f'pack[{i}]')
            pack_quantity = request.data.get(f'pack_quantity[{i}]')

            if pack_title and pack_image:
                product_pack = ProductPackage.objects.create(
                    product_id=product.id,
                    title=json.loads(pack_title),
                    image=pack_image,
                    quantity=pack_quantity
                )
                i += 1
                total_quantity += pack_quantity
            else:
                break

        for i in range(4):
            product_image = request.data.get(f'image[{i}]')

            if product_image:
                image = ProductImage.objects.create(
                    product_id=product.id,
                    image=product_image
                )
            else:
                break
        product.title = title
        product.category_id = category
        product.description = description
        product.price = price
        product.buy_price = buy_price
        if total_quantity > 0:
            product.in_stock = total_quantity
        else:
            product.in_stock = quantity
        product.save()

        return Response({"type": "success", "message": "Product updated successfully"})


class CouponView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        if request.user.user_type == "VENDOR":
            serializer = CouponSerializer()
            data = serializer.get_data(request.user.id)
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "There is no coupons for you"})

    def post(self, request):
        if request.user.user_type == "VENDOR":
            product_id = request.data.get('product_id')
            code = request.data.get('code')
            value = request.data.get('value')
            end_date = request.data.get('end_date')

            if not product_id or not code or not value or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            end_date = end_date.split("-")
            coupon = Coupon.objects.create(
                product_id=product_id,
                code=code,
                value=value,
                end_date=date(
                    int(end_date[0]),
                    int(end_date[1]),
                    int(end_date[2])+1
                ),
            )
            return Response({"type": "success", "message": "coupon created successfully"})
        return Response({"type": "error", "message": "There is no coupons for you"})

    def delete(self, request):
        if request.user.user_type == "VENDOR":
            coupon_id = request.data.get("id")
            if not coupon_id:
                return Response({"type": "error", "message": "can't delete coupon"})
            coupon = Coupon.objects.filter(
                id=coupon_id, product__user__id=request.user.id)
            if not coupon.exists():
                return Response({"type": "error", "data": "Coupon not found"})
            coupon = coupon.get()
            coupon.delete()
            return Response({"type": "success", "message": "coupon was deleted"})
        return Response({"type": "error", "message": "There is no coupons for you"})

    def put(self, request):
        if request.user.user_type == "VENDOR":
            coupon_id = request.data.get('id')
            product_id = request.data.get('product_id')
            code = request.data.get('code')
            value = request.data.get('value')
            end_date = request.data.get('end_date')
            if not coupon_id or not product_id or not code or not value or not end_date:
                return Response({"type": "error", "message": "complete missing data"})

            coupon = Coupon.objects.filter(
                id=coupon_id, product__user__id=request.user.id)
            if not coupon.exists():
                return Response({"type": "error", "data": "Coupon not found"})
            end_date = end_date.split("-")

            coupon = coupon.get()
            coupon.product_id = product_id
            coupon.code = code
            coupon.value = value
            coupon.end_date = date(
                int(end_date[0]),
                int(end_date[1]),
                int(end_date[2])+1
            )
            coupon.save()
            return Response({"type": "success", "message": "coupon updated successfully"})
        return Response({"type": "error", "message": "There is no coupons for you"})


class DiscountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        serializer = DiscountSerializer()
        data = serializer.get_data(request.user.id)
        return Response({"type": "success", "data": list(data)})

    def post(self, request):
        if request.user.user_type == "VENDOR":
            product_id = request.data.get('product_id')
            title = request.data.get('title')
            percentage = request.data.get('percentage')
            end_date = request.data.get('end_date')

            product_runing_duscoutns = Discount.objects.filter(
                product_id=product_id,
                end_date__gt=timezone.now()
            )

            if len(product_runing_duscoutns) >= 1:
                if len(product_runing_duscoutns) >= 2:
                    product_runing_duscoutns[1:].delete()
                return Response({"type": "error", "message": "Product already have runing discounts"})

            if not product_id or not title or not percentage or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            end_date = end_date.split("-")
            discount = Discount.objects.create(
                product_id=product_id,
                title=title,
                percentage=percentage,
                end_date=date(
                    int(end_date[0]),
                    int(end_date[1]),
                    int(end_date[2])+1
                ),
            )
            return Response({"type": "success", "message": "discount created successfully"})
        return Response({"type": "error", "message": "There is no discounts for you"})

    def delete(self, request):
        if request.user.user_type == "VENDOR":
            discount_id = request.data.get("id")
            if not discount_id:
                return Response({"type": "error", "message": "can't delete discount"})
            discount = Discount.objects.filter(
                id=discount_id, product__user__id=request.user.id)
            if not discount.exists():
                return Response({"type": "error", "data": "discount not found"})
            discount = discount.get()
            discount.delete()
            return Response({"type": "success", "message": "discount was deleted"})
        return Response({"type": "error", "message": "There is no discounts for you"})

    def put(self, request):
        if request.user.user_type == "VENDOR":
            discount_id = request.data.get('id')
            product_id = request.data.get('product_id')
            title = request.data.get('title')
            percentage = request.data.get('percentage')
            end_date = request.data.get('end_date')
            if not discount_id or not product_id or not title or not percentage or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            end_date = end_date.split("-")
            discount = Discount.objects.filter(
                id=discount_id, product__user__id=request.user.id)
            if not discount.exists():
                return Response({"type": "error", "data": "discount not found"})
            discount = discount.get()
            discount.product_id = product_id
            discount.title = title
            discount.percentage = percentage
            discount.end_date = date(
                int(end_date[0]),
                int(end_date[1]),
                int(end_date[2])+1
            )
            discount.save()
            return Response({"type": "success", "message": "discount updated successfully"})
        return Response({"type": "error", "message": "There is no discounts for you"})


class GetCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_all_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "Something went wrong, try later"})


class GetProductDetailsView(APIView):
    permission_classes = [HasOwner]
    authentication_classes = [UserTokenBackend]

    def get(self, request, id):
        serializer = ProductSerializer()
        data = serializer.get_product_details(id)
        return Response({"type": "success", "data": data})


class GetReviewsView(APIView):
    def get(self, request, id):
        serializer = ReviewsSerializer()
        stats = serializer.get_reviews_stats(id)
        reviews = serializer.get_reviews(id)
        return Response({"type": "success", "data": {"stats": stats, "reviews": reviews}})


User = get_user_model()


class DashboardDataView(APIView):
    def get(self, request):
        data = {}
        data['products'] = Product.objects.filter(
            user__id=request.user.id).count()
        data['orders'] = Order.objects.filter(
            product__user__id=request.user.id,
            status="DELEVRED"
        ).count()
        data['reviews'] = Review.objects.filter(
            product__user__id=request.user.id).count()
        data['sales'] = Order.objects.filter(
            status="DELEVRED",
            product__user__id=request.user.id
        ).aggregate(earning=Sum("price"))['earning']
        print(data['sales'])

        return Response({"type": "success", "data": data})

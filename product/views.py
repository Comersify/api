from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer, ReviewsSerializer, CouponSerializer, DiscountSerializer
from django.db.models import Q
from .models import Coupon, Discount
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend


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
    def get(self, request):
        try:
            serializer = ProductSerializer()
            products = serializer.get_products()
            keyword = request.GET.get('q')
            price_from = int(request.GET.get('from')) if request.GET.get(
                'from') else request.GET.get('from')
            price_to = int(request.GET.get('to')) if request.GET.get(
                'to') else request.GET.get('to')
            stars = int(request.GET.get('stars'))
            categories = request.GET.get(
                'categories').replace(" ", "").split(",")
            orderby = request.GET.get('orderBy')
            if keyword:
                print(f"length os {len(products)}")
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
            return Response({"type": "success", "data": products})
        except Exception as e:
            print(e)
            return Response({"type": "error", "message": "Something went wrong try later"})


class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request, id=None):
        if request.user.user_type == "VENDOR":
            serializer = ProductSerializer()
            data = serializer.get_product_details_for_vendor(request.user.id, id)
            if not id:
                return Response({"type": "error", "message": "Product id is missing"})
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
        print(request.data)
        return Response({"type": "error", "data": "not developed yet "})

    def delete(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def put(self, request):
        return Response({"type": "error", "data": "not developed yet "})


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
            coupon = Coupon.objects.create(
                product=product_id,
                code=code,
                value=value,
                end_date=end_date,
            )
            return Response({"type": "success", "message": "coupon created successfully"})
        return Response({"type": "error", "message": "There is no coupons for you"})

    def delete(self, request):
        if request.user.user_type == "VENDOR":
            coupon_id = request.data.get("id")
            if not coupon_id:
                return Response({"type": "error", "message": "can't delete coupon"})
            coupon = Coupon.objects.filter(
                id=coupon_id, product__store__user__id=request.user.id)
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
                id=coupon_id, product__store__user__id=request.user.id)
            if not coupon.exists():
                return Response({"type": "error", "data": "Coupon not found"})
            coupon = coupon.get()
            coupon.product_id = product_id
            coupon.code = code
            coupon.value = value
            coupon.end_date = end_date
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
            if not product_id or not title or not percentage or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            discount = Discount.objects.create(
                product=product_id,
                title=title,
                percentage=percentage,
                end_date=end_date,
            )
            return Response({"type": "success", "message": "discount created successfully", "data": discount})
        return Response({"type": "error", "message": "There is no discounts for you"})

    def delete(self, request):
        if request.user.user_type == "VENDOR":
            discount_id = request.data.get("id")
            if not discount_id:
                return Response({"type": "error", "message": "can't delete discount"})
            discount = Discount.objects.filter(
                id=discount_id, product__store__user__id=request.user.id)
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

            discount = Discount.objects.filter(
                id=discount_id, product__store__user__id=request.user.id)
            if not discount.exists():
                return Response({"type": "error", "data": "discount not found"})
            discount = discount.get()
            discount.product_id = product_id
            discount.title = title
            discount.percentage = percentage
            discount.end_date = end_date
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

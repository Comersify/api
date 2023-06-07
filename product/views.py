from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer, ReviewsSerializer


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
            q = request.GET.get('q')
            price_from = request.GET.get('price_from')
            price_to = request.GET.get('price_to')
            stars = int(request.GET.get('stars'))
            categories = request.GET.get(
                'categories').replace(" ", "").split(",")
            orderby = request.GET.get('orderBy')
            if price_from:
                products = products.filter(act_price__gte=price_from)
            if price_to:
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
            return Response({"type": "error", "message": "Something went wrong try later"})


class CreateProductView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class DeleteProductView(APIView):
    def post(self, request, id):
        return Response({"type": "error", "data": "not developed yet "})


class UpdateProductView(APIView):
    def post(self, request, id):
        return Response({"type": "error", "data": "not developed yet "})


class GetCouponView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class CreateCouponView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class DeleteCouponView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class UpdateCouponView(APIView):
    def post(self, request, id):
        return Response({"type": "error", "data": "not developed yet "})


class GetCouponByCodeView(APIView):
    def get(self, request, code):
        return Response({"type": "error", "data": "not developed yet "})


class GetDiscountView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class CreateDiscountView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class DeleteDiscountView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class UpdateDiscountView(APIView):
    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})


class GetMyProductsView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})


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

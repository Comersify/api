from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer


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
            print(data)
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetProductsView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})


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
        return Response({"type": "error", "data": "not developed yet "})


class GetProductDetailsView(APIView):
    def get(self, request, id):
        return Response({"type": "error", "data": "not developed yet "})


class GetReviewsView(APIView):
    def get(self, request, product_id):
        return Response({"type": "error", "data": "not developed yet "})

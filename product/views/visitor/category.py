from rest_framework.response import Response
from rest_framework.views import APIView
from product.serializers import CategorySerializer


class GetHotCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_hot_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_all_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "Something went wrong, try later"})
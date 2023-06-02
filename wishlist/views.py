from rest_framework.response import Response
from rest_framework.views import APIView


class GetWishListDetailsView(APIView):
    def get(request):
        return Response({"type": "error", "message": "Not developed yet"})


class AddProductToWishListView(APIView):
    def post(request):
        return Response({"type": "error", "message": "Not developed yet"})


class DeleteProductFromWishList(APIView):
    def post(request):
        return Response({"type": "error", "message": "Not developed yet"})

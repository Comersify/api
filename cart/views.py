from rest_framework.response import Response
from rest_framework.views import APIView


class GetCartDetailsView(APIView):
    def get(request, id):
        return Response({"type": "error", "message": "not developed yet"})


class AddProoductToCartView(APIView):
    def post(request):
        return Response({"type": "error", "message": "not developed yet"})


class DeleteProoductFromCartView(APIView):
    def post(request):
        return Response({"type": "error", "message": "not developed yet"})


class UpdateProoductInCartView(APIView):
    def post(request):
        return Response({"type": "error", "message": "not developed yet"})

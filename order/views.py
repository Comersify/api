from rest_framework.response import Response
from rest_framework.views import APIView


class GetMyOrdersView(APIView):
    def get(request):
        return Response({"type": "error", "message": "not developed yet"})


class CreateOrderView(APIView):
    def get(request):
        return Response({"type": "error", "message": "not developed yet"})

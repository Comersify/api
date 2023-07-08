from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product, Review
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from django.db.models import Sum
from order.models import Order


class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

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

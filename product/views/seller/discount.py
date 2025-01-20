from rest_framework.response import Response
from rest_framework.views import APIView
from product.serializers import DiscountSerializer
from product.models import Discount
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from datetime import date
from django.utils import timezone

class DiscountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        serializer = DiscountSerializer()
        data = serializer.get_data(request.user.id)
        return Response({"type": "success", "data": list(data)})

    def post(self, request):
        if request.user.user_type != "CUSTOMER":
            product_id = request.data.get('product_id')
            discounted_price = request.data.get('discounted_price')
            end_date = request.data.get('end_date')

            product_runing_duscoutns = Discount.objects.filter(
                product_id=product_id,
                end_date__gt=timezone.now()
            )

            if len(product_runing_duscoutns) >= 1:
                if len(product_runing_duscoutns) >= 2:
                    product_runing_duscoutns[1:].delete()
                return Response({"type": "error", "message": "Product already have runing discounts"})

            if not product_id or not discounted_price or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            end_date = end_date.split("-")
            discount = Discount.objects.create(
                product_id=product_id,
                discounted_price=discounted_price,
                end_date=date(
                    int(end_date[0]),
                    int(end_date[1]),
                    int(end_date[2])+1
                ),
            )
            return Response({"type": "success", "message": "discount created successfully"})
        return Response({"type": "error", "message": "There is no discounts for you"})

    def delete(self, request):
        if request.user.user_type != "CUSTOMER":
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
        if request.user.user_type != "CUSTOMER":
            discount_id = request.data.get('id')
            product_id = request.data.get('product_id')
            discounted_price = request.data.get('discounted_price')
            end_date = request.data.get('end_date')
            if not discount_id or not product_id or not discounted_price or not end_date:
                return Response({"type": "error", "message": "complete missing data"})
            end_date = end_date.split("-")
            discount = Discount.objects.filter(
                id=discount_id, product__user__id=request.user.id)
            if not discount.exists():
                return Response({"type": "error", "data": "discount not found"})
            discount = discount.get()
            discount.product_id = product_id
            discount.discounted_price = discounted_price
            discount.end_date = date(
                int(end_date[0]),
                int(end_date[1]),
                int(end_date[2])+1
            )
            discount.save()
            return Response({"type": "success", "message": "discount updated successfully"})
        return Response({"type": "error", "message": "There is no discounts for you"})

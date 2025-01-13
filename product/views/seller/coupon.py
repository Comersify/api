from rest_framework.views import APIView
from product.serializers import CouponSerializer
from product.models import Coupon
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from rest_framework.response import Response
from datetime import date
from core.backend import UserTokenBackend

class CouponView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def get(self, request):
        if request.user.user_type != "CUSTOMER":
            serializer = CouponSerializer()
            data = serializer.get_data(request.user.id)
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "There is no coupons for you"})

    def post(self, request):
        if request.user.user_type != "CUSTOMER":
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
        if request.user.user_type != "CUSTOMER":
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
        if request.user.user_type != "CUSTOMER":
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

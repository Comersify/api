from rest_framework.response import Response
from product.models import Discount, Shipping
from rest_framework.views import APIView
from user.models import ShippingInfo
from cart.models import ShoppingCart
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from .models import Order
from .serializers import OrderSerializer
from django.utils import timezone


class GetMyOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        try:
            orders = Order.objects.filter(user_id=request.user.id).exclude(status='IN_CART').values(
                'id', 'product__title', 'quantity', 'price', 'status', 'created_at')
            data = list(orders)
            return Response({"type": "success", "data": data})
        except:
            return Response({'type': 'error', 'message': 'Something went wrong try later'})


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        try:
            address = request.data.get('address')
            phone_number = request.data.get('phoneNumber')
            postal_code = request.data.get('postalCode')
            shipping_id = request.data.get("shippingID")
            if not address or not phone_number or not postal_code or not shipping_id:
                return Response({"type": "error", "message": "Please enter all needed informations"})

            info = ShippingInfo.objects.filter(
                user_id=request.user.id,
                address=address,
                phone_number=phone_number,
                postal_code=postal_code
            )
            shipping_info_id = None
            if not info.exists():
                info = ShippingInfo.objects.create(
                    user_id=request.user.id,
                    address=address,
                    phone_number=phone_number,
                    postal_code=postal_code
                )
                shipping_info_id = info.id
            else:
                info = info.get()
                shipping_info_id = info.id

            cart = ShoppingCart.objects.filter(
                user_id=request.user.id
            )
            if not cart.exists():
                return Response({'type': 'error', 'message': 'No orders found'})
            cart = cart.get()
            orders = cart.orders.all()
            if len(orders) <= 0:
                return Response({'type': 'error', 'message': 'No orders found'})
            shipping = Shipping.objects.filter(user_id=request.user.id, id=id)
            for order in orders:
                order.status = "SUBMITTED"
                order.shipping_info_id = shipping_info_id
                order.shipping = shipping
                price = order.product.price - shipping.price
                discount = Discount.objects.filter(
                    product_id=order.product.id, end_date__gt=timezone.now())
                if discount.exists():
                    discount = discount.get()
                    price -= (price * discount.percentage / 100)
                price = price * order.quantity
                if order.coupon:
                    price -= order.coupon.value
                order.price = price
                order.created_at = timezone.now()
                order.save()
            cart.orders.clear()
            cart.save()
            return Response({'type': 'success', 'message': 'Your was submitted wait the seller to shipe it'})
        except:
            return Response({'type': 'error', 'message': 'Something went wrong try later'})


class VendorOrdersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        if request.user.user_type == "VENDOR":
            serializer = OrderSerializer()
            data = serializer.get_data(request.user.id)
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "User not valid"})

    def put(self, request):
        return Response({"type": "error", "message": "not developed yet"})

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShoppingCart
from order.models import Order
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from core.backend import AccessTokenBackend


class GetCartDetailsView(APIView):
    def get(request, id):
        return Response({"type": "error", "message": "not developed yet"})


class AddProoductToCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def create_order(self, request):
        order = Order.objects.create(
            user_id=request.user.id,
            product_id=request.data["product_id"],
            pack_id=request.data["pack_id"],
            quantity=1,
            status="IN_CART",
        )
        return order

    @csrf_exempt
    def post(self, request):
        print(request.data)
        cart = ShoppingCart.objects.filter(user_id=request.user.id)
        if cart.exists():
            in_cart = cart.filter(
                orders__product__id=request.data['product_id'])
            if len(in_cart) > 0:
                return Response({"type": "error", "message": "Product already in cart"})
            else:
                order = self.create_order(request)
                cart = cart.get()
                cart.orders.add(order)
                return Response({"type": "success", "message": "Product added to cart"})
        else:
            order = self.create_order(request)
            cart = ShoppingCart.objects.create(
                user_id=request.user.id,
            )
            cart.orders.add(order)
            return Response({"type": "success", "message": "Product added to cart"})


class DeleteProoductFromCartView(APIView):
    def post(request):
        return Response({"type": "error", "message": "not developed yet"})


class UpdateProoductInCartView(APIView):
    def post(request):
        return Response({"type": "error", "message": "not developed yet"})

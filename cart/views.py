from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShoppingCart
from product.models import Coupon
from order.models import Order
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from core.backend import AccessTokenBackend
from .serializers import ShoppingCartSerializer


class GetCartDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        serializer = ShoppingCartSerializer()
        data = serializer.get_data(id=request.user.id)
        return Response({"type": "success", "data": data})


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
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        order_id = request.data.get("order_id")
        if not order_id:
            return Response({"type": "error", "message": "Data is missing"})
        cart = ShoppingCart.objects.filter(user_id=request.user.id)
        if not cart.exists():
            return Response({"type": "error", "message": "Cart doesn't exist"})
        cart = cart.get()
        order = cart.orders.filter(id=order_id)
        if not order.exists():
            return Response({"type": "error", "message": "Order doesn't exist"})
        order.delete()
        return Response({"type": "success", "message": "Product deleted from your cart"})


class UpdateProoductInCartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        order_id = request.data.get("order_id")
        quantity = request.data.get("quantity")
        if not order_id or not quantity or quantity <= 0:
            return Response({"type": "error", "message": "Data is missing"})
        cart = ShoppingCart.objects.filter(user_id=request.user.id)
        if not cart.exists():
            return Response({"type": "error", "message": "Cart doesn't exist"})
        cart = cart.get()
        order = cart.orders.filter(id=order_id)
        if not order.exists():
            return Response({"type": "error", "message": "Order doesn't exist"})
        order = order.get()
        order.quantity = quantity
        order.save()
        return Response({"type": "success", "message": "Product deleted from your cart"})


class ApplyCouponView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({"type": "error", "message": "Data is missing"})
        cart = ShoppingCart.objects.filter(user_id=request.user.id)
        if not cart.exists():
            return Response({"type": "error", "message": "Data is missing"})
        cart = cart.get()
        ids = cart.orders.all().select_related('product').values('product__id')
        ids = [id['product__id'] for id in ids]
        coupon = Coupon.objects.filter(product_id__in=ids).filter(code=code)
        if not coupon.exists():
            return Response({"type": "error", "message": "Coupon not valid"})
        coupon = coupon.select_related('product').get()
        order = cart.orders.filter(product_id=coupon.product.id).get()
        order.coupon = coupon
        order.save()
        return Response({"type": "success", "data": {"coupon__code": order.coupon.code, "coupon__percentage": order.coupon.percentage, "product__price": order.product.price}})

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WishList
from product.models import Product
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from .seriliazes import WishListSerializer


class GetWishListDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        serializer = WishListSerializer()
        data = serializer.get_data(request.user.id)
        if data:
            return Response({"type": "success", "data": data})
        return Response({"type": "success", "data": []})


class ProductInWishListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request, id):
        wish_list = WishList.objects.filter(user_id=request.user.id)
        if wish_list.exists():
            wish_list = wish_list.get()
            data = wish_list.products.filter(id=id).exists()
            return Response({"type": "success", "data": data})
        return Response({"type": "success", "data": False})


class AddProductToWishListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        wish_list = WishList.objects.filter(user_id=request.user.id)
        product = Product.objects.filter(id=request.data['product_id'])
        if not product.exists():
            return Response({"type": "error", "message": "Product doesn't exist"})
        product = product.get()
        if wish_list.exists():
            in_wish_list = wish_list.filter(
                products__id=request.data['product_id'])
            if len(in_wish_list) > 0:
                return Response({"type": "error", "message": "Product already in your list"})
            else:
                wish_list = wish_list.get()
                wish_list.products.add(product)
                return Response({"type": "success", "message": "Product added to your list"})
        else:
            wish_list = WishList.objects.create(
                user_id=request.user.id,
            )
            wish_list.products.add(product)
            return Response({"type": "success", "message": "Product added to your list"})


class DeleteProductFromWishList(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def post(self, request):
        wish_list = WishList.objects.filter(user_id=request.user.id)
        product = Product.objects.filter(id=request.data['product_id'])
        if not product.exists():
            return Response({"type": "error", "message": "Product doesn't exist"})
        product = product.get()
        if wish_list.exists():
            wish_list = wish_list.get()
            wish_list.products.remove(product)
            return Response({"type": "success", "message": "Product removed from your list"})
        else:
            return Response({"type": "success", "message": "Product is not in your list"})

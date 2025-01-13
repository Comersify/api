from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WishList
from product.models import Product
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from .seriliazes import WishListSerializer
from datetime import datetime
from core.backend import UserTokenBackend

class GetWishListDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def get(self, request):
        serializer = WishListSerializer()
        data = serializer.get_data(request.user.id)
        if data:
            return Response({"type": "success", "data": data})
        return Response({"type": "success", "data": []})


class ProductInWishListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def get(self, request, id):
        wish_list = WishList.objects.filter(user_id=request.user.id)
        if wish_list.exists():
            wish_list = wish_list.get()
            data = wish_list.products.filter(id=id).exists()
            return Response({"type": "success", "data": data})
        return Response({"type": "success", "data": False})


class AddProductToWishListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

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
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

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

from django.http import HttpResponse


def index(request):
    html = f'''
    <html>
    <head>
    <title style="color: green;">Comercify</title>
    </head>
        <body
            style="
            user-select:none;
            height: 100%; padding: 0; margin: 0;
            display:flex; justify-content: center; align-items:center;
        background-image: linear-gradient(to right, #ff4b96, #6056ff);
           "
        >
         <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="
                color:white; height:80px; width:80px; font-weight: bold; margin-right: 10px;
            "><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 21v-7.5a.75.75 0 01.75-.75h3a.75.75 0 01.75.75V21m-4.5 0H2.36m11.14 0H18m0 0h3.64m-1.39 0V9.349m-16.5 11.65V9.35m0 0a3.001 3.001 0 003.75-.615A2.993 2.993 0 009.75 9.75c.896 0 1.7-.393 2.25-1.016a2.993 2.993 0 002.25 1.016c.896 0 1.7-.393 2.25-1.016a3.001 3.001 0 003.75.614m-16.5 0a3.004 3.004 0 01-.621-4.72L4.318 3.44A1.5 1.5 0 015.378 3h13.243a1.5 1.5 0 011.06.44l1.19 1.189a3 3 0 01-.621 4.72m-13.5 8.65h3.75a.75.75 0 00.75-.75V13.5a.75.75 0 00-.75-.75H6.75a.75.75 0 00-.75.75v3.75c0 .415.336.75.75.75z"></path></svg> 
            
            <h1 style="
            font-size: 50px;
            color:white; font-weight:bold; font-family: sans;
            ">Comercify API</h1>
        </body>
    </html>
    '''
    return HttpResponse(html)
from rest_framework.views import APIView
from product.serializers import ProductSerializer
from product.models import Product, ProductImage, ProductPackage
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from rest_framework.response import Response
import json


class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request, id):
        if request.user.user_type == "VENDOR":
            serializer = ProductSerializer()
            data = serializer.get_product_details_for_vendor(
                request.user.id, id)
            if not data:
                return Response({"type": "error", "message": "Product not found"})
            return Response({"type": "success", "data": data})
        return Response({"type": "error", "message": "user not valid"})


class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request):
        if request.user.user_type == "VENDOR":
            serializer = ProductSerializer()
            data = serializer.get_products_for_vendor(request.user.id)
            if not data:
                return Response({"type": "error", "message": "Product not found"})
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "user not valid"})

    def post(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        data = request.data.get('data')
        if data is None:
            return Response({"type": "error", "message": "Pls complete your product information"})

        data = json.loads(data)
        title = data.get('title')
        category_id = data.get('category')
        price = data.get('price')
        buy_price = data.get('buy_price')
        description = data.get('description')
        quantity = data.get('quantity')

        if not buy_price or not title or not category_id or not price or not description or not quantity:
            return Response({"type": "error", "message": "Pls complete your product information"})
        if not quantity and not request.data.get('pack_quantity[0]') and not request.data.get('title[0]') and not request.data.get('pack[0]'):
            return Response({"type": "error", "message": "Complete needed information"})

        if not store.exists():
            return Response({"type": "error", "message": "Can't create product"})
        store = store.get()
        product = Product.objects.create(
            store_id=request.user.id,
            title=title,
            category_id=category_id,
            price=price,
            buy_price=buy_price,
            description=description,
            in_stock=quantity,
        )

        if request.data.get('image[0]') is None:
            return Response({"type": "error", "message": "Product image is missing"})

        i = 0
        total_quantity = 0
        while True:
            pack_title = request.data.get(f'title[{i}]')
            pack_image = request.data.get(f'pack[{i}]')
            pack_quantity = request.data.get(f'quantity[{i}]')
            if pack_title and pack_image:
                product_pack = ProductPackage.objects.create(
                    product_id=product.id,
                    title=json.loads(pack_title),
                    image=pack_image
                )
                i += 1
                total_quantity += pack_quantity
            else:
                break
        if total_quantity > 0:
            product.in_stock = total_quantity
        for i in range(4):
            product_image = request.data.get(f'image[{i}]')

            if product_image:
                image = ProductImage.objects.create(
                    product_id=product.id,
                    image=product_image
                )
            else:
                break

        return Response({"type": "success", "message": "product created successfully "})

    def delete(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        product_id = request.data.get('id')
        if product_id is None:
            return Response({"type": "error", "message": "data is missing"})
        product = Product.objects.filter(
            user__id=request.user.id, id=product_id
        )
        if not product.exists():
            return Response({"type": "error", "message": "Product not found"})
        product.delete()
        return Response({"type": "success", "message": "Product was deleted"})

    def put(self, request):
        if request.user.user_type != "VENDOR":
            return Response({"type": "error", "message": "user not valid"})
        data = request.data.get('data')

        if data is None:
            return Response({"type": "error", "message": "data is missing"})

        data = json.loads(data)
        product_id = data.get("id")
        title = data.get("title")
        category = data.get("category")
        description = data.get("description")
        price = data.get("price")
        buy_price = data.get("buy_price")
        quantity = data.get("quantity")
        images = data.get("images")
        packs = data.get("packs")

        if not buy_price or not product_id or not title or not category or not description or not price:
            return Response({"type": "error", "message": "Complete needed information"})
        if not quantity and not request.data.get('pack_quantity[0]') and not request.data.get('title[0]') and not request.data.get('pack[0]'):
            return Response({"type": "error", "message": "Complete needed information"})

        product = Product.objects.filter(
            user__id=request.user.id,
            id=product_id
        )
        if not product.exists():
            return Response({"type": "error", "message": "Product not found"})
        product = product.get()

        deleted_product_images = ProductImage.objects.filter(
            product_id=product.id).exclude(id__in=images)
        deleted_product_packs = ProductPackage.objects.filter(
            product_id=product.id).exclude(id__in=packs)
        deleted_product_images.delete()
        deleted_product_packs.delete()
        i = 0
        total_quantity = 0
        while True:
            pack_title = request.data.get(f'title[{i}]')
            pack_image = request.data.get(f'pack[{i}]')
            pack_quantity = request.data.get(f'quantity[{i}]')
            print(pack_quantity)
            if pack_title and pack_image:
                product_pack = ProductPackage.objects.create(
                    product_id=product.id,
                    title=json.loads(pack_title),
                    image=pack_image,
                    quantity=pack_quantity
                )
                i += 1
                total_quantity += int(pack_quantity)
            else:
                break

        for i in range(4):
            product_image = request.data.get(f'image[{i}]')

            if product_image:
                image = ProductImage.objects.create(
                    product_id=product.id,
                    image=product_image
                )
            else:
                break
        product.title = title
        product.category_id = category
        product.description = description
        product.price = price
        product.buy_price = buy_price
        if total_quantity > 0:
            product.in_stock = total_quantity
        else:
            product.in_stock = quantity
        product.save()

        return Response({"type": "success", "message": "Product updated successfully"})

from rest_framework.views import APIView
from product.serializers import ProductSerializer
from product.models import Category, Product, ProductImage, Packaging
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.backend import AccessTokenBackend
from rest_framework.response import Response
import json

from product.serializers.category import CategorySerializer



class ProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]

    def get(self, request, id):
        if request.user.user_type != "CUSTOMER":
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
    auth_users = ["VENDOR", "INDIVIDUAL-SELLER"]

    def get(self, request):
        if request.user.user_type != "CUSTOMER":
            serializer = ProductSerializer()
            data = serializer.get_products_for_vendor(request.user.id)
            if not data:
                return Response({"type": "error", "message": "Product not found"})
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "user not valid"})

    def post(self, request):
        if request.user.user_type not in self.auth_users:
            return Response({"type": "error", "message": "user not valid"})
        data = request.data.get('data')
        if data is None:
            return Response({"type": "error", "message": "Pls complete your product information"})

        data = json.loads(data)
        title = data.get('title')
        category_id = data.get('category')
        price = data.get('price')
        buy_price = data.get('buy_price') or None
        description = data.get('description')
        quantity = data.get('quantity') or None
        related_product_id = data.get("relatedProductId")
        packaging = data.get("packaging")

        if not title or not category_id or not price or not description:
            return Response({"type": "error", "message": "Pls complete your product information"})
        if request.data.get('image[0]') is None:
            return Response({"type": "error", "message": "Product image is missing"})

        product = Product.objects.create(
            user_id=request.user.id,
            title=title,
            category_id=category_id,
            price=price,
            buy_price=buy_price,
            description=description,
            in_stock=quantity,
            related_product_id=related_product_id
        )
        for pack_id in packaging:
            try:
                pack = Packaging.objects.filter(id=pack_id).get()
                product.packaging.add(pack)
            except:
                pass
        
        product.save()
        
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
        if request.user.user_type not in self.auth_users:
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
        if request.user.user_type not in self.auth_users:
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
        related_product_id = data.get("relatedProductId")

        if not product_id or not title or not category or not description or not price:
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
        deleted_product_images.delete()
        
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
        product.related_product_id = related_product_id
        product.category_id = category
        product.description = description
        product.price = price
        product.buy_price = buy_price
        product.quantity = quantity
        product.save()

        return Response({"type": "success", "message": "Product updated successfully"})

class CategoriesView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [AccessTokenBackend]
    auth_users = ["INDIVIDUAL-SELLER"]

    def get(self, request):
        try:
            print(request.user)
            print(request.domain)
            serializer = CategorySerializer(request.user.id or request.owner.id)
            data = serializer.get_all_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "Something went wrong, try later"})

    def post(self, request):
        try:
            if request.user and request.user.user_type in self.auth_users:
                category = Category.objects.create(
                    user_id=request.user.id,
                    name=request.data['name'],
                )
                if parent_id := request.data.get('parentID'):
                    category.parent_id = int(parent_id)
                category.save()
            return Response({"type": "success", "message": "Category created"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})

    def put(self, request):
        try:
            if request.user and request.user.user_type in self.auth_users:
                category = Category.objects.filter(
                    user_id=request.user.id,
                    id=request.data['id'],
                )
                if not category.exists():
                    return Response({"type": "error", "message": "user not valid"})
                category = category.get()
                if parent_id := request.data.get('parentID'):
                    category.parent_id = int(parent_id)
                category.name=request.data['name']
                category.save()
            return Response({"type": "success", "message": "Category updated"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})

    def delete(self, request):
        try:
            if request.user and request.user.user_type in self.auth_users:
                category = Category.objects.filter(
                    user_id=request.user.id,
                    name=request.data['name'],
                )
                if not category.exists():
                    return Response({"type": "error", "message": "user not valid"})
                category = category.get()
                category.delete()
            return Response({"type": "success", "message": "Category delted"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})

class PackageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend]
    auth_users = ["INDIVIDUAL-SELLER"]

    def get(self, request):
        try:
            if request.user.user_type in self.auth_users:
                obj = Packaging.objects.filter(user_id=request.user.id)
                data = list(obj.values('id', 'name'))
                return Response({"type": "success", "data": data})
            return Response({"type": "error", "message": "user not valid"})
        except:
            return Response({"type": "error", "message": "Something went wrong, try later"})

    def post(self, request):
        try:
            if request.user.user_type in self.auth_users:
                packaging = Packaging.objects.create(
                    user_id=request.user.id,
                    name=request.data['name'],
                )
                packaging.save()
                return Response({"type": "success", "message": "Packaging created"})
            return Response({"type": "error", "message": "user not valid"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})
    
    def put(self, request):
        try:
            if request.user.user_type in self.auth_users:
                packaging = Packaging.objects.filter(
                    user_id=request.user.id,
                    id=request.data['id'],
                )
                if not packaging.exists():
                    return Response({"type": "error", "message": "user not valid"})
                packaging = packaging.get()
                packaging.name = request.data['name']
                packaging.save()
                return Response({"type": "success", "message": "Packaging updated"})
            return Response({"type": "error", "message": "user not valid"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})

    def delete(self, request):
        try:
            if request.user.user_type in self.auth_users:
                packaging = Packaging.objects.filter(
                    user_id=request.user.id,
                    id=request.data['id'],
                )
                if not packaging.exists():
                    return Response({"type": "error", "message": "user not valid"})
                packaging = packaging.get()
                packaging.delete()
                return Response({"type": "success", "message": "Packaging deleted"})
            return Response({"type": "error", "message": "user not valid"})
        except Exception as e:
            return Response({"type": "error", "message": str(e)})
    
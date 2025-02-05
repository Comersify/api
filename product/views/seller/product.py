from rest_framework.views import APIView
from product.serializers import ProductSerializer, VisitorProductSerializer, VendorProductSerializer
from product.models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.backend import AccessTokenBackend
from rest_framework.response import Response
import json
from rest_framework import viewsets
from product.serializers.category import CategorySerializer
from product.serializers.variant import *
from permissions import IsIndividualSeller

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
        )
        
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

        product.title = title
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
            user_id = request.user.id if request.user else request.owner.id
            serializer = CategorySerializer(user_id)
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



class AttributeViewSet(viewsets.ModelViewSet):
    """API for managing Attributes (e.g., Color, Size, Month)"""
    permission_classes = [IsIndividualSeller]
    serializer_class = AttributeSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        return Attribute.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

class AttributeValueViewSet(viewsets.ModelViewSet):
    """API for managing Attribute Values (e.g., Red, Large, January)"""
    authentication_classes = [AccessTokenBackend]
    serializer_class = AttributeValueSerializer
    permission_classes = [IsIndividualSeller]
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        attr_id = self.request.GET.get('attrId')
        queryset = AttributeValue.objects.filter(attribute__user=self.request.user)

        if attr_id:
            queryset = queryset.filter(attribute_id=attr_id)
        
        return queryset

class ProductViewSet(viewsets.ModelViewSet):
    """API for managing Products"""
    queryset = Product.objects.all()
    authentication_classes = [AccessTokenBackend]
    serializer_class = ProductSerializer
    auth_users = ["INDIVIDUAL-SELLER"]

    def get_queryset(self):
        if self.request.user:
            return Product.objects.filter(user=self.request.user)
        else:
            return Product.objects.filter(user=self.request.owner)
        
    def get_permissions(self):
        if self.request.method == "GET":  # Only allow admins to create products
            return [AllowAny()]
        return [IsIndividualSeller()]
    
    def get_serializer_class(self):
        """Use different serializers for admins and regular users"""
        if self.request.user.user_type in self.auth_users:  # Admins get more data
            return VendorProductSerializer
        return VisitorProductSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    

class ProductVariantViewSet(viewsets.ModelViewSet):
    """API for managing Product Variants"""
    queryset = ProductVariant.objects.all()
    authentication_classes = [AccessTokenBackend]
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']
    auth_users = ["INDIVIDUAL-SELLER"]

class ProductViewSet(viewsets.ModelViewSet):
    """API for managing Product Variants"""
    queryset = ProductVariant.objects.all()
    authentication_classes = [AccessTokenBackend]
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticated, AllowAny]
    http_method_names = ['get', 'post', 'put', 'delete']
    auth_users = ["INDIVIDUAL-SELLER"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  
    
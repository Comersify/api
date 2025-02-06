from rest_framework.response import Response
from rest_framework.views import APIView
from product.serializers import CategorySerializer, CategorySerializerV2
from core.backend import AccessTokenBackend
from product.models import Category
from rest_framework import viewsets
from permissions import IsIndividualSeller
from rest_framework.permissions import AllowAny

class GetHotCategoriesView(APIView):

    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_hot_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})



class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializerV2
    authentication_classes = [AccessTokenBackend]
    http_method_names = ['get', 'post', 'put', 'delete']
    
    def get_queryset(self):
        query = Category.objects.filter(parent=None)
        if self.request.user:
            query = query.filter(user=self.request.user)
        else:
            query = query.filter(user=self.request.owner)
        return query

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsIndividualSeller()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
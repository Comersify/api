from rest_framework.views import APIView
from product.serializers import ProductSerializer, IndividualSellerProductSerializer
from core.backend import UserTokenBackend
from rest_framework.response import Response
from django.db.models import Q
from user.models import CustomUser


class GetProductsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        if request.owner.user_type == CustomUser.TypeChoices.INDIVIDUAL_SELLER:
            serializer = IndividualSellerProductSerializer(request)
            products = serializer.get_products()
            return Response({"type": "success", "data": products})

        serializer = ProductSerializer()
        products = serializer.get_products()
        keyword = request.GET.get('q')
        offset = int(request.GET.get("offset")) if request.GET.get(
            "offset") else False
        price_from = int(request.GET.get('from')) if request.GET.get(
            'from') else False
        price_to = int(request.GET.get('to')) if request.GET.get(
            'to') else False
        stars = int(request.GET.get('stars')) if request.GET.get(
            'stars') else False
        categories = request.GET.get(
            'categories').replace(" ", "").split(",") if request.GET.get(
            'categories') else ['']
        orderby = request.GET.get('orderBy')
        if keyword:
            products = products.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword)
            )
        if price_from != '' and price_from > 0:
            products = products.filter(act_price__gte=price_from)
        if price_to != '' and price_to > 0:
            products = products.filter(act_price__lte=price_to)
        if stars > 0:
            products = products.filter(reviews__gte=stars)
        if categories != ['']:
            categories = [int(cat) for cat in categories]
            products = products.filter(category_id__in=categories)
        if orderby:
            if orderby == "act_price":
                products = products.order_by(orderby)
            else:
                products = products.order_by(f"-{orderby}")

        paginate_from = False
        paginate_to = False
        if offset:
            paginate_to = offset * 10
            paginate_from = paginate_to - 10
            products = products[paginate_from:paginate_to]

        return Response({"type": "success", "data": products[:15]})


class GetProductDetailsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request, id):
        serializer = ProductSerializer()
        data = serializer.get_product_details(id)
        return Response({"type": "success", "data": data})



class GetSuperDealsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        try:
            serializer = ProductSerializer()
            data = serializer.get_super_deals()
            return Response({"type": "success", "data": data})
        except Exception as e:
            return Response({"type": "error", "data": str(e)})


class GetNewProductsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        try:
            serializer = ProductSerializer()
            data = serializer.get_new_products()
            return Response({"type": "success", "data": data})
        except Exception as e:
            return Response({"type": "error", "data": str(e)})


class GetBestSellersView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        try:
            serializer = ProductSerializer()
            data = serializer.get_best_sellers()
            return Response({"type": "success", "data": data})
        except Exception as e:
            return Response({"type": "error", "data": str(e)})

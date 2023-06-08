from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, CategorySerializer, ReviewsSerializer
from django.db.models import Q


class GetSuperDealsView(APIView):
    def get(self, request):
        try:
            serializer = ProductSerializer()
            data = serializer.get_super_deals()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetHotCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_hot_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "data": "Something went wrong try later"})


class GetProductsView(APIView):
    def get(self, request):
        try:
            serializer = ProductSerializer()
            products = serializer.get_products()
            keyword = request.GET.get('q')
            price_from = int(request.GET.get('from')) if request.GET.get(
                'from') else request.GET.get('from')
            price_to = int(request.GET.get('to')) if request.GET.get(
                'to') else request.GET.get('to')
            stars = int(request.GET.get('stars'))
            categories = request.GET.get(
                'categories').replace(" ", "").split(",")
            orderby = request.GET.get('orderBy')
            if keyword:
                print(f"length os {len(products)}")
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
            return Response({"type": "success", "data": products})
        except Exception as e:
            print(e)
            return Response({"type": "error", "message": "Something went wrong try later"})


class ProductView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def delete(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def update(self, request):
        return Response({"type": "error", "data": "not developed yet "})



class CouponView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def delete(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def update(self, request):
        return Response({"type": "error", "data": "not developed yet "})




class DiscountView(APIView):
    def get(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def post(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def delete(self, request):
        return Response({"type": "error", "data": "not developed yet "})

    def update(self, request):
        return Response({"type": "error", "data": "not developed yet "})



class GetCategoriesView(APIView):
    def get(self, request):
        try:
            serializer = CategorySerializer()
            data = serializer.get_all_categories()
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "Something went wrong, try later"})


class GetProductDetailsView(APIView):
    def get(self, request, id):
        serializer = ProductSerializer()
        data = serializer.get_product_details(id)
        return Response({"type": "success", "data": data})


class GetReviewsView(APIView):
    def get(self, request, id):
        serializer = ReviewsSerializer()
        stats = serializer.get_reviews_stats(id)
        reviews = serializer.get_reviews(id)
        return Response({"type": "success", "data": {"stats": stats, "reviews": reviews}})

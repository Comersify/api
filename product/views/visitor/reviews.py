from rest_framework.response import Response
from rest_framework.views import APIView
from product.serializers import ReviewsSerializer


class GetReviewsView(APIView):
    def get(self, request, id):
        serializer = ReviewsSerializer()
        stats = serializer.get_reviews_stats(id)
        reviews = serializer.get_reviews(id)
        return Response({"type": "success", "data": {"stats": stats, "reviews": reviews}})

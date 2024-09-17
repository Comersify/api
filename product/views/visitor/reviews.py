from rest_framework.response import Response
from rest_framework.views import APIView
from product.serializers import ReviewsSerializer
from core.backend import UserTokenBackend


class GetReviewsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request, id):
        serializer = ReviewsSerializer()
        stats = serializer.get_reviews_stats(id)
        reviews = serializer.get_reviews(id)
        return Response({"type": "success", "data": {"stats": stats, "reviews": reviews}})

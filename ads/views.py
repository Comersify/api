from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AdsSerializer
from .models import Ads


class GetAdsView(APIView):
    def get(self, request):
        query = Ads.objects.all()
        serializer = AdsSerializer(query, many=True)
        return Response({"type": "success", "data": serializer.data})

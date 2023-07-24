from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AdsSerializer
from .models import Ads
from core.backend import UserTokenBackend
from permissions import HasOwner

class GetAdsView(APIView):
    permission_classes = [HasOwner]
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        query = Ads.objects.all()
        serializer = AdsSerializer(query, many=True)
        return Response({"type": "success", "data": serializer.data})

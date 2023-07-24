from rest_framework.views import APIView, Response
from .models import Tracker
from core.backend import UserTokenBackend
from permissions import HasOwner

class CreateTracker(APIView):
    permission_classes = [HasOwner]
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        tracker = Tracker.objects.create()
        return Response({"type": "success", "data": tracker.id})

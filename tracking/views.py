from rest_framework.views import APIView, Response
from .models import Tracker
from core.backend import UserTokenBackend

class CreateTracker(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        tracker = Tracker.objects.create()
        return Response({"type": "success", "data": tracker.id})

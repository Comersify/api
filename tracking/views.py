from rest_framework.views import APIView, Response
from .models import Tracker


class CreateTracker(APIView):

    def get(self, request):
        tracker = Tracker.objects.create()
        return Response({"type": "success", "data": tracker.id})

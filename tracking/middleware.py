from .models import Tracker, Visit


class TrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user_agent = request.META.get('HTTP_USER_AGENT')
        trackID = request.META.get('X-Comercify-Visitor')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get(
            'HTTP_CLIENT_IP', '') or request.META.get('REMOTE_ADDR', '')
        logged_in = False
        if request.META.get('Authorization'):
            logged_in = True
        if trackID:
            Visit.objects.create(
                tracker__id=trackID,
                client_url="blob",
                client_path="blob",
                api_path="blob",
                browser=user_agent,
                ip_address=ip_address,
                logged_in=logged_in,
            )

        response = self.get_response(request)

        return response

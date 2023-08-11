from .models import Visit


class TrackerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user_agent = request.META.get('HTTP_USER_AGENT')
        trackID = request.META.get('HTTP_X_COMERCIFY_VISITOR')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '') or request.META.get(
            'HTTP_CLIENT_IP', '') or request.META.get('REMOTE_ADDR', '')
        logged_in = False

        if request.META.get('HTTP_AUTHORIZATION'):
            logged_in = True

        client_url = request.META.get('HTTP_ORIGIN')
        api_path = request.META.get('PATH_INFO')
        print("###########")
        print(trackID)
        if trackID:
            Visit.objects.create(
                tracker_id=trackID,
                client_url=client_url,
                client_path="blob",
                api_path=api_path,
                browser=user_agent,
                ip_address=ip_address,
                logged_in=logged_in,
            )

        response = self.get_response(request)

        return response

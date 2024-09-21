from .models import Visit
from website.models import Website

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
        if trackID:
            try:
                Visit.objects.create(
                    tracker_id=trackID,
                    client_url=client_url,
                    client_path="blob",
                    api_path=api_path,
                    browser=user_agent,
                    ip_address=ip_address,
                    logged_in=logged_in,
                )
            except Exception as e:
                print(e)

        response = self.get_response(request)

        return response


class SubDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        sub_domain = request.META.get("HTTP_ORIGIN", "").split(".")[0]
        sub_domain = sub_domain.replace("https://", "").replace("http://", "")
        if sub_domain:
            site = Website.objects.filter(sub_domain=sub_domain)
            if site.exists():
                request.owner = site.get().user
            else:
                request.owner = Website.objects.filter(sub_domain="demo").get().user

        response = self.get_response(request)
        return response



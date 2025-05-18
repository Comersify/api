from django.contrib.auth import get_user_model
import json
from core.backend import AccessTokenBackend
from utils import set_cookies
User = get_user_model()

class TokenToUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.owner = ''
        refresh = False
        if '/admin' in request.get_full_path():
            return self.get_response(request)

        _, refresh = AccessTokenBackend().authenticate(request)

        domain = request.META.get("HTTP_ORIGIN", "")
        print(domain)
        domain = domain.replace("https://", "").replace("http://", "")
        print(domain)
        if domain:
            site = Website.objects.filter(Q(domain=domain) | Q(test_domain=domain))
            if site.exists():
                request.owner = site.get().user
            else:
                request.owner = Website.objects.filter(domain="demo").get().user

        try:
            if request.body:
                request.data = json.loads(request.body)
        except:
            pass

        response = self.get_response(request)
        if refresh:
            set_cookies(refresh,response)
        return response


"""
class TokenInjectionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the user is authenticated and there is no token in the response already
        if request.user.is_authenticated:
            tokens = get_tokens_for_user(request.user)
            # Adding tokens to the response headers
            response["X-Access-Token"] = tokens['access']
            response["X-Refresh-Token"] = tokens['refresh']

        return response
"""

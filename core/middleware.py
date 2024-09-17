from django.contrib.auth import get_user_model
import json
from core.backend import AccessTokenBackend, UserTokenBackend
User = get_user_model()


class TokenToUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.owner = ''
        refresh = False
        # Check if the authorization header is present
        if 'Authorization' in request.headers:
            # Use JWTAuthentication to authenticate the token
            user, refresh = AccessTokenBackend().authenticate(request)
        
        #if 'X-Comercify-Owner' in request.headers:
        #    # Use JWTAuthentication to authenticate the token
        #    UserTokenBackend().authenticate(request)

        try:
            if request.body:
                request.data = json.loads(request.body)
        except:
            pass

        response = self.get_response(request)
        if refresh:
            response.set_cookie(
                'cify_access',
                str(refresh.access_token),
                max_age=3600,
                httponly=True,
                secure=True,
                samesite='None'
            )
            response.set_cookie(
                'cify_refresh',
                str(refresh),
                max_age=3600,
                httponly=True,
                secure=True,
                samesite='None'
            )
            response.set_cookie(
                'cify_exp',
                refresh.payload['exp'],
                max_age=3600,
                httponly=True,
                secure=True,
                samesite='None'
            )
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

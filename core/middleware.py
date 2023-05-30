from django.contrib.auth import get_user_model
import json
from core.backend import AccessTokenBackend
User = get_user_model()


class TokenToUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.headers)
        # Check if the authorization header is present
        if 'Authorization' in request.headers:
            # Use JWTAuthentication to authenticate the token
            AccessTokenBackend().authenticate(request)

        if request.body:
            try:
                request.data = json.loads(request.body)
            except:
                pass
        # Process the request
        response = self.get_response(request)

        return response
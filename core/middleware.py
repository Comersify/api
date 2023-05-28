from rest_framework_simplejwt.authentication import JWTAuthentication


class TokenToUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the authorization header is present
        if 'Authorization' in request.headers:
            # Use JWTAuthentication to authenticate the token
            jwt_auth = JWTAuthentication()
            # Returns a tuple (user, token)
            user, _ = jwt_auth.authenticate(request)
            print(user)
            # Assign the user to request.user
            request.user = user if user.is_authenticated else None

        # Process the request
        response = self.get_response(request)

        return response

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from user.models import Token

User = get_user_model()


class AccessTokenBackend(JWTAuthentication):
    def authenticate(self, request):
        try:
            token = request.headers['Authorization']
            decoded_token = self.get_validated_token(token)
            user = User.objects.filter(id=decoded_token['user_id']).get()
            request.user = user
        except InvalidToken:
            return None

        return (user, token)


class UserTokenBackend:

    def authenticate_header(self, request):
        try:
            if request.owner:
                return True
        except: 
            pass

        if 'X-Comercify-Owner' in request.headers:
            return True
        return False

    def authenticate(self, request):
        try:
            token = request.headers.get(
                'X-Comercify-Owner')
            if not token:
                return None
            token = Token.objects.filter(token=token).get()
            request.owner = token.user
        except Exception as e:
            print(e)
            return None

        return (token.user, token)

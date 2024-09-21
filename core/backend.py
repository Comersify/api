from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model
from user.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
User = get_user_model()


class AccessTokenBackend(JWTAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get('cify_access','')
            timestamp = request.COOKIES.get('cify_exp','')
            refresh = request.COOKIES.get('cify_access','')
            exp = datetime.fromtimestamp(int(timestamp))
            
            if exp > datetime.now() and token:
                decoded_token = self.get_validated_token(token)
                user = self.get_user(decoded_token)
                request.user = user
                return (user, None)
            
            if exp < datetime.now() and refresh:
                refresh = RefreshToken(refresh_token)
                user_id = token.payload['user_id']
                user = User.objects.filter(id=user_id).get()
                request.user = user
                return (user, token)
        except Exception:
            return (None, None)

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

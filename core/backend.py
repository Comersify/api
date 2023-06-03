from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model

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

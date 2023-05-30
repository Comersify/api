from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import get_user_model

User = get_user_model()


class AccessTokenBackend(JWTAuthentication):
    def authenticate(self, request):
        try:
            decoded_token = self.get_validated_token(
                request.headers['Authorization'])
            user = User.objects.filter(id=decoded_token['user_id']).get()
            request.user = user

        except InvalidToken:
            return None

        return (user, None)

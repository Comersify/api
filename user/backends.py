from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Authenticate against email OR username.
    Allows admin login with either email or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None
        
        # Try to find user by email first, then by username
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password):
            return user
        return None

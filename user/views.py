from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.backend import AccessTokenBackend
from django.views.decorators.csrf import csrf_exempt
from .serializers import StoreSerializer
from .models import AppReviews
from .serializers import CustomersSerializer
from .providers import sign_with_google
from core.backend import UserTokenBackend
from utils import set_cookies

User = get_user_model()


class SignUpWithProviderView(APIView):
    authentication_classes = [UserTokenBackend]
    
    def post(self, request, provider):
        token = request.data.get("token")
        user_type = request.data.get("userType")
        if not token:
            return Response({"type": "error", "message": "Couldn't find your email try again"})
        if provider == "google":
            user_token = sign_with_google(token, user_type)
            if not user_token:
                return Response({"type": "error", "message": "Couldn't find your email try again"})
            response = Response({"type": "success", "data": {'name':user_token['name']}})
            return set_cookies(user_token['token'],response)
        return Response({"type": "error", "message": "Provider not found"})


class ResetPasswordView(APIView):
    authentication_classes = [UserTokenBackend]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"type": "error", "message": "email is missing"})
        user = User.objects.filter(email=email)
        if user.exists():
            return Response({"type": "error", "message": "Email not related to any user"})
        sent = True
        if sent:
            return Response({"type": "success", "message": "Check your email reset password link was sent"})
        else:
            return Response({"type": "error", "message": "Something went wrong try later"})


class SettingsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def get(self, request):
        user = User.objects.filter(id=request.user.id)
        if not user.exists():
            return Response({"type": "error", "message": "user not fount"})
        user = user.get()

        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
        }
        if user.image:
            data["image"] = user.image.url
        return Response({"type": "success", "data": data})


class UpdateSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def post(self, request):
        import json
        user = User.objects.filter(id=request.user.id)
        if not user.exists():
            return Response({"type": "error", "message": "User not found"})
        user = user.get()
        image = request.data.get('file')
        data = None
        if image:
            data = json.loads(request.data.get('json_data'))
        else:
            data = request.data
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        old_password = data.get('oldPassword')
        new_password = data.get('password')
        password_confermation = data.get('passwordConfermation')
        if len(request.data.keys()) < 0:
            return Response({'type': 'error', 'message': 'No updates found'})
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        if image:
            user.image.delete()
            user.image.save(image.name, image)
        if old_password and new_password and password_confermation:
            if not user.check_password(old_password) or new_password != password_confermation:
                return Response({'type': 'error', 'message': 'password not valid'})
            user.set_password(new_password)
        user.save()
        return Response({'type': 'success', 'message': 'Your account information updated successfully'})


class LoginView(APIView):
    authentication_classes = [UserTokenBackend]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                "type": "success",
                "name": user.first_name
            }
            if user.image:
                response_data['image'] = user.image.url
            response = Response(response_data)
            set_cookies(refresh, response)
            return response
        else:
            return Response({"type": 'error', "message": 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    authentication_classes = [UserTokenBackend]

    
    def post(self, request):
        refresh = request.data.get('refresh')
        if refresh:
            token = RefreshToken(refresh)
            access = str(token.access_token)
            user_id = token.payload['user_id']
            user = User.objects.filter(id=user_id).get()
            image = None
            if user.image:
                image = user.image.url
            return Response({"type": "success", "refresh": refresh, "access": access, 'exp': token.payload['exp'], 'image': image, "name": user.first_name})
        else:
            return Response({"type": "error", "message": "invalid token"})


class SignupView(APIView):
    authentication_classes = [UserTokenBackend]
    
    @csrf_exempt
    def post(self, request):
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        password = request.data.get('password')
        password_confermation = request.data.get("passwordConfermation")
        email = request.data.get('email')
        phone_number = request.data.get('phoneNumber')

        if not last_name or not phone_number or not first_name or not password or not email or not password_confermation:
            return Response({"type": 'error', "message": 'Please provide missing fields'})

        if User.objects.filter(email=email).exists():
            return Response({"type": 'error', "message": 'Username is already taken.'})

        if password != password_confermation:
            return Response({"type": "error", "message": "password not match"})

        user = User.objects.create_user(
            user_type="CUSTOMER",
            username=email.split("@")[0],
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            is_active=True,
            phone_number=phone_number
        )
        return Response({'type': 'success', 'message': 'User created successfully.'})


class GetStoreByIDView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request, id):
        serializer = StoreSerializer()
        data = serializer.get_store_details(id)
        if data:
            return Response({'type': 'success', 'data': data})
        return Response({'type': 'error', 'message': "Store not found"})


class GetTopStorseView(APIView):
    authentication_classes = [UserTokenBackend]
    
    def get(self, request):
        try:
            serializer = StoreSerializer()
            data = serializer.get_top_stores()
            return Response({'type': 'success', 'data': data})
        except:
            return Response({'type': 'error', 'message': 'Something went wrong refresh the page'})


class GetAppReviewsView(APIView):
    authentication_classes = [UserTokenBackend]

    def get(self, request):
        try:
            query = AppReviews.objects.all()[:5]
            data = list(query)
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "Something went wrong try later"})


class GetCustomersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [AccessTokenBackend, UserTokenBackend]

    def get(self, request):
        if request.user.user_type != "CUSTOMER":
            serializer = CustomersSerializer()
            data = serializer.get_data(request.user.id)
            return Response({"type": "success", "data": list(data)})
        return Response({"type": "error", "message": "user not valid"})

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .models import Store
from product.serializers import ProductSerializer
from product.models import Review
from order.models import Order

User = get_user_model()


class SettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.filter(id=request.user.id).get()
            data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
            }
            if user.image:
                data["image"] = user.image
            return Response({"type": "success", "data": data})
        except:
            return Response({"type": "error", "message": "user not fount"})


class UpdateSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.POST:
            data = request.data
        return Response({"type": "success", "message": "test"})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            response_data = {
                "type": "success",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response_data)
        else:
            return Response({"type": 'error', "message": 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        if refresh:
            token = RefreshToken(refresh)
            access = str(token.access_token)
            return Response({"type": "success", "refresh": refresh, "access": access})
        else:
            return Response({"type": "error", "message": "invalid token"})


class SignupView(APIView):

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
            phone_number=phone_number
        )
        return Response({'type': 'success', 'message': 'User created successfully.'})


class GetStoreByIDView(APIView):
    def get(self, request, id):
        sotre = Store.objects.filter(id=id)
        if store.exists():
            store = sotre.get()
        else:
            return Response({'type': 'error', 'message': "Store not found"})
        orders = Order.objects.filter(product__store__id=id).count()
        reviews = Review.objects.filter(product__store__id=id).count()
        data = {
            "cover": sotre.cover.url,
            "logo": sotre.logo.url,
            "name": sotre.name,
            "description": sotre.description,
            "orders": orders,
            "reviews": reviews,
            "products": ProductSerializer().get_data(store_id=id)
        }
        return Response({'type': 'success', 'data': data})


class GetTopStorseView(APIView):
    def get(self, request):
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def get_app_reviews(request):
    return


def get_addresse(requesr):
    return


def create_addresse(request):
    return

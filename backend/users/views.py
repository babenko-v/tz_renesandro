from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from rest_framework import status
from .serializer import UserRegisterSerializer
from rest_framework.response import Response
from .utils import generate_tokens_and_set_cookie
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Вызываем функцию для генерации токенов и установки cookie
            return generate_tokens_and_set_cookie(user)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return JsonResponse({'error': 'Refresh token not found'}, status=status.HTTP_401_UNAUTHORIZED)

        data = {'refresh': refresh_token}
        request.data = data

        return super().post(request, *args, **kwargs)

class UserRegistrationView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return generate_tokens_and_set_cookie(user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
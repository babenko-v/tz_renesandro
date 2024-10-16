from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse
from rest_framework import status
from .serializer import UserRegisterSerializer
from rest_framework.response import Response
from .utils import generate_tokens_and_set_cookie
from django.contrib.auth import get_user_model
from .models import UserModel
from .serializer import UserSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
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



class DetailUser(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if not request.COOKIES.get('refresh_token'):
            return Response({"detail": "No tokens provided."}, status=status.HTTP_400_BAD_REQUEST)


        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        return response
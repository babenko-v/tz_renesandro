from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserRegistrationView, DetailUser, LogoutView

app_name = 'identification'

urlpatterns = [

    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('user/', DetailUser.as_view(), name='user'),
]
from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, UserRegistrationView

app_name = 'identification'

urlpatterns = [

    # path('logout/', views.logout_view, name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
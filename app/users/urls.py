from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # login
    TokenRefreshView,     # refresh
    TokenBlacklistView,    # logout
    TokenVerifyView
)
from .views import AuthInitView, LoginView
urlpatterns = [
    path('register/', AuthInitView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='otp-login'),
]
urlpatterns += [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
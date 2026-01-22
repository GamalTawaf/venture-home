from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


# handles user authentication and token generation
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

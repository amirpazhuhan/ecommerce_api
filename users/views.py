from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import CustomTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Create your views here.

user = get_user_model()


class RegisterView(generics.CreateAPIView):

    queryset = user.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    pass


class MeView(generics.RetrieveUpdateAPIView):
    """Return or update only the authenticated customer's own profile."""

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

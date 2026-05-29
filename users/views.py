from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializer import UserSerializer
from django.contrib.auth import get_user_model

# Create your views here.

user = get_user_model()
    
class RegisterView(generics.CreateAPIView):
    
    queryset = user.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
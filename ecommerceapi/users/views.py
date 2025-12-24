from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegisterSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny


class UserCreateView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        return Response(user_data, status=HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        login_data = request.data
        serializer = self.serializer_class(data=login_data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=login_data['username'], password=login_data['password'])

        if not user:
            raise AuthenticationFailed('Wrong Credentials')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled')

        login(request, user)
        return Response(status=HTTP_200_OK)

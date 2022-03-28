from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('clients/create/', UserCreateView.as_view()),
    path('auth/login/', UserLoginView.as_view())
]

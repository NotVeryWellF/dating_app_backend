from rest_framework import serializers
from .models import User
import datetime
from django.db import models


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)
    username = serializers.CharField(min_length=3, max_length=64)
    email = serializers.EmailField(min_length=3, max_length=256)
    first_name = serializers.CharField(min_length=3, max_length=64)
    last_name = serializers.CharField(min_length=3, max_length=64)
    birth_date = serializers.DateField()

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters',
        'first_name': 'The first_name should only contain letters',
        'last_name': 'The last_name should only contain letters',
        'birth_date': 'Birth date cannot be in the future'
    }

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'gender', 'avatar']

    def validate(self, attrs):
        username = attrs.get('username', '')
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')
        birth_date = attrs.get('birth_date', '')

        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages['username'])

        if not first_name.isalpha():
            raise serializers.ValidationError(self.default_error_messages['first_name'])

        if not last_name.isalpha():
            raise serializers.ValidationError(self.default_error_messages['last_name'])

        if birth_date >= datetime.date.today():
            raise serializers.ValidationError(self.default_error_messages['birth_date'])

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=64)
    password = serializers.CharField(min_length=8, max_length=64, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


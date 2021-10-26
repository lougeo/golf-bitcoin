from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = settings.AUTH_USER_MODEL.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )
        return user

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Friendship, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["sender", "receiver", "accepted"]

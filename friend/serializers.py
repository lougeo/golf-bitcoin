from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import GolfUser

from .models import Friendship, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        required=False, queryset=GolfUser.objects.all()
    )

    class Meta:
        model = FriendRequest
        fields = ["sender", "receiver", "accepted"]

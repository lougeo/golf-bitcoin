from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from users.models import GolfUser
from users.serializers import UserSerializer

from .models import Friendship, FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(
        required=False, queryset=GolfUser.objects.all()
    )
    sender_full = UserSerializer(read_only=True, source="sender")

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "sender_full", "receiver", "accepted"]

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        if instance:
            self.fields["receiver"].required = False

    def update(self, instance, validated_data):
        accepted = validated_data["accepted"]
        if accepted:
            instance.accept()
        else:
            instance.decline()

        return instance

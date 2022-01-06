from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from friend.models import FriendRequest

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(
        label=_("Confirm Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "password_confirm")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        return user

    def validate(self, data):
        """
        Check that passwords match.
        """
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password": "Passwords don't match!",
                }
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    is_friend = serializers.SerializerMethodField()
    has_pending_request = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "date_joined",
            "is_friend",
            "has_pending_request",
        ]

    def get_is_friend(self, obj):
        request = self.context.get("request")
        return request.user.friends.filter(pk=obj.pk).exists() if request else None

    def get_has_pending_request(self, obj):
        request = self.context.get("request")
        return (
            FriendRequest.objects.filter(
                sender=request.user, receiver=obj, active=True
            ).exists()
            if request
            else None
        )

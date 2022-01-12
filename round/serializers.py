from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from course.models import Course, Scorecard
from course.serializers import (
    CourseSerializer,
    ScorecardSerializer,
    MinCourseSerializer,
)
from users.models import GolfUser
from users.serializers import UserSerializer

from .models import Round, Registration, Score


class RoundSerializer(serializers.ModelSerializer):
    course = MinCourseSerializer(read_only=True)
    scorecard = ScorecardSerializer(read_only=True)
    users = UserSerializer(many=True, read_only=True)

    set_course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
    set_scorecard = serializers.PrimaryKeyRelatedField(
        queryset=Scorecard.objects.all(), write_only=True
    )
    set_users = serializers.PrimaryKeyRelatedField(
        queryset=GolfUser.objects.all(), many=True, write_only=True, required=False
    )

    class Meta:
        model = Round
        fields = "__all__"

    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        if self.instance:
            self.fields["set_course"].required = False
            self.fields["set_scorecard"].required = False

    def create(self, validated_data):
        request = self.context.get("request")
        users = [request.user.pk]
        # Remove set_ names
        course = validated_data.pop("set_course")
        scorecard = validated_data.pop("set_scorecard")
        users.extend(validated_data.pop("set_users", []))
        # Add proper names
        validated_data.update(
            {
                "course": course,
                "scorecard": scorecard,
                "users": users,
            }
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        users = [request.user.pk]
        users.extend(validated_data.pop("set_users", []))
        validated_data.update({"users": users})
        return super().update(instance, validated_data)

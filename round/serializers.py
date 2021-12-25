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
        queryset=GolfUser.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Round
        fields = "__all__"

    def create(self, validated_data):
        # Remove set_ names
        course = validated_data.pop("set_course")
        scorecard = validated_data.pop("set_scorecard")
        users = validated_data.pop("set_users")
        # Add proper names
        validated_data.update(
            {
                "course": course,
                "scorecard": scorecard,
                "users": users,
            }
        )
        return super().create(validated_data)

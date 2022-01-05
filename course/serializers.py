from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Course, Scorecard, ScorecardHole


class ScorecardHoleSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = ScorecardHole
        exclude = ["scorecard"]


class ScorecardSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    scorecard_holes = ScorecardHoleSerializer(many=True)

    class Meta:
        model = Scorecard
        fields = "__all__"

    def create(self, validated_data):
        scorecardholes_data = validated_data.pop("scorecard_holes")
        scorecard = super().create(validated_data)
        for scorecardhole_data in scorecardholes_data:
            ScorecardHole.objects.create(scorecard=scorecard, **scorecardhole_data)
        return scorecard

    def update(self, instance, validated_data):
        # slightly more complicated so going to leave for now
        scorecardholes_data = validated_data.pop("scorecard_holes")
        scorecard = super().update(instance, validated_data)
        for scorecardhole_data in scorecardholes_data:
            # print(scorecardhole_data)
            # pk = scorecardhole_data.pop("pk")
            number = scorecardhole_data.pop("number")
            obj, created = ScorecardHole.objects.update_or_create(
                scorecard=scorecard, number=number, defaults=scorecardhole_data
            )

        return scorecard


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    scorecards = ScorecardSerializer(many=True)

    class Meta:
        model = Course
        fields = "__all__"


class MinCourseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

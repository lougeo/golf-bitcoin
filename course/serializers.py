from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

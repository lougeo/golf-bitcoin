from rest_framework import viewsets

from .models import Course, Scorecard, ScorecardHole
from .serializers import CourseSerializer, ScorecardSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class ScorecardViewSet(viewsets.ModelViewSet):
    queryset = Scorecard.objects.all()
    serializer_class = ScorecardSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned scorecards to a specified course.
        """
        course_id = self.request.query_params.get("course")
        if course_id is not None:
            queryset = self.queryset.filter(course_id=course_id)
        else:
            queryset = self.queryset
        return queryset

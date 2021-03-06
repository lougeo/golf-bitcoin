from rest_framework import viewsets

from .filters import CourseFilter
from .models import Course, Scorecard, ScorecardHole
from .paginators import CoursePaginator
from .serializers import CourseSerializer, MinCourseSerializer, ScorecardSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    filterset_class = CourseFilter
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseSerializer
        else:
            return MinCourseSerializer


class ScorecardViewSet(viewsets.ModelViewSet):
    queryset = Scorecard.objects.all()
    serializer_class = ScorecardSerializer
    pagination_class = CoursePaginator

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

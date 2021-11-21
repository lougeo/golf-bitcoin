from django.urls import path, include

from rest_framework import routers

from .viewsets import CourseViewSet, ScorecardViewSet

app_name = "course"

router = routers.SimpleRouter()
router.register("courses", CourseViewSet)
router.register("scorecards", ScorecardViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

from django.urls import path, include

from rest_framework import routers

from .viewsets import RoundViewSet

app_name = "round"

router = routers.SimpleRouter()
router.register("rounds", RoundViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

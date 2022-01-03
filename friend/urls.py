from django.urls import path, include

from rest_framework import routers

from .viewsets import FriendRequestViewSet

app_name = "friend"

router = routers.SimpleRouter()
router.register("friendrequests", FriendRequestViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]

from django.urls import path, include
from knox import views as knox_views

from rest_framework import routers

from .viewsets import LoginAPI, RegistrationAPI, UserAPI, UserViewSet

app_name = "users"

router = routers.SimpleRouter()
router.register("users", UserViewSet)

urlpatterns = [
    # API paths
    path("api/auth/user/", UserAPI.as_view(), name="user_detail"),
    path("api/auth/login/", LoginAPI.as_view(), name="api_login"),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="api_logout"),
    path(
        "api/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="api_logoutall"
    ),
    path("api/auth/register/", RegistrationAPI.as_view(), name="api_register"),
    # Router paths
    path("api/", include(router.urls)),
]

from django.urls import path
from knox import views as knox_views

from . import views
from .viewsets import LoginAPI, RegistrationAPI, TokenValidationAPI

app_name = "users"

urlpatterns = [
    # API urls
    path(
        "api/auth/token-validation/",
        TokenValidationAPI.as_view(),
        name="api_token_validation",
    ),
    path("api/auth/login/", LoginAPI.as_view(), name="api_login"),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="api_logout"),
    path(
        "api/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="api_logoutall"
    ),
    path("api/auth/register/", RegistrationAPI.as_view(), name="api_register"),
]

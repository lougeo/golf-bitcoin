from django.urls import path
from knox import views as knox_views

from . import views
from .viewsets import APILoginView

app_name = "users"

urlpatterns = [
    # API urls
    path("api/auth/login/", APILoginView.as_view(), name="api_login"),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="api_logout"),
    path(
        "api/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="api_logoutall"
    ),
]

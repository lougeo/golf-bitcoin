import datetime
import json
from django.contrib.auth import login
from django.db.models import Q

from rest_framework import viewsets, views, permissions, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import permissions

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from friend.models import FriendshipStatus

from .models import GolfUser
from .paginators import UserPaginator
from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    LoginSerializer,
)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=format)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # Will raise a 401 if authentication fails (except in the case of bad key format)
        # This method will both delete any expired tokens, and renew valid ones
        valid = TokenAuthentication().authenticate(request)

        if valid:
            user, auth_token = valid
            return Response(UserSerializer(user).data)
        else:
            raise AuthenticationFailed("Invalid Token.")


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GolfUser.objects.all().order_by("first_name")
    serializer_class = UserSerializer
    pagination_class = UserPaginator

    def get_queryset(self):
        search = self.request.GET.get("search")
        selected_users = [
            int(id) for id in json.loads(self.request.GET.get("selected-users"))
        ]
        selected_users.append(self.request.user.pk)
        declined_status = FriendshipStatus.objects.declined()

        return (
            GolfUser.objects.prefetch_related("friendships__status")
            .exclude(pk__in=selected_users)
            .exclude(friendship__status=declined_status)
            .filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
            )
            .order_by("first_name")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

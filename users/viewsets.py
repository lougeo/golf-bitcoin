from django.contrib.auth import login

from rest_framework import viewsets, permissions, generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import permissions

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from .serializers import CreateUserSerializer, UserSerializer, AuthTokenSerializer


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.data)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


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

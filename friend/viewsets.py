from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Friendship, FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    @action(detail=False)
    def mine(self, request):
        queryset = self.filter_queryset(
            FriendRequest.objects.filter(receiver=request.user, active=True)
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data.update({"sender": request.user.pk})
        return super().create(request, *args, **kwargs)

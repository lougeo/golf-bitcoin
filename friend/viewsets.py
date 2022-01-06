from rest_framework import viewsets


from .models import Friendship, FriendRequest
from .serializers import FriendRequestSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request, *args, **kwargs):
        request.data.update({"sender": request.user.pk})
        return super().create(request, *args, **kwargs)

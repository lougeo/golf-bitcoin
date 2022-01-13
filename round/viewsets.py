from rest_framework import viewsets


from .models import Round, Registration, Score
from .serializers import RoundSerializer


class RoundViewSet(viewsets.ModelViewSet):
    """
    TODO: Restrict update to creator.
    """

    queryset = Round.objects.all()
    serializer_class = RoundSerializer

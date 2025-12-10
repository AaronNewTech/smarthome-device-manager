from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from server.apps.rooms.models import Room
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """Simple Room API - read/write for rooms."""
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

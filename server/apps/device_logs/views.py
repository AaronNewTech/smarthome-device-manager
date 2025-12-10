from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from server.apps.device_logs.models import DeviceLog
from .serializers import DeviceLogSerializer


class DeviceLogViewSet(viewsets.ModelViewSet):
    queryset = DeviceLog.objects.all().order_by('-timestamp')
    serializer_class = DeviceLogSerializer
    permission_classes = [AllowAny]

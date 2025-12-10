from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from server.apps.device_categories.models import DeviceCategory
from .serializers import DeviceCategorySerializer


class DeviceCategoryViewSet(viewsets.ModelViewSet):
    queryset = DeviceCategory.objects.all().order_by('name')
    serializer_class = DeviceCategorySerializer
    permission_classes = [AllowAny]

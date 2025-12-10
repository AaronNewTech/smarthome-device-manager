import logging

from django.db import IntegrityError, transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers as drf_serializers
from rest_framework.exceptions import APIException

from .serializers import DeviceSerializer
from server.apps.device_logs.serializers import DeviceLogSerializer
from server.apps.device_logs.models import DeviceLog
from .models import Device

logger = logging.getLogger(__name__)


class DeviceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Device model.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=["get", "post"], url_path="logs")
    def logs(self, request, pk=None):
        """Handle logs for a specific device.

        - GET /api/v1/devices/{pk}/logs/  -> list logs (newest first)
        - POST /api/v1/devices/{pk}/logs/ -> create a new log for device
        """
        # get_object() will raise 404 if not found and applies any view-level
        # permission checks.
        device = self.get_object()

        if request.method == 'GET':
            qs = DeviceLog.objects.filter(device=device).order_by("-timestamp")

            # respect pagination if configured on the view/router
            page = self.paginate_queryset(qs)
            if page is not None:
                serializer = DeviceLogSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = DeviceLogSerializer(qs, many=True)
            return Response(serializer.data)

        # POST: create a new log for this device
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        if 'change_type' in data and 'action' not in data:
            data['action'] = data.pop('change_type')

        serializer = DeviceLogSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save(device=device)
        except IntegrityError:
            logger.exception("IntegrityError when creating DeviceLog for device %s", device.id)
            raise drf_serializers.ValidationError({"detail": "Database integrity error while creating device log."})
        except Exception:
            logger.exception("Unexpected error when creating DeviceLog for device %s", getattr(device, 'id', None))
            raise APIException("Internal server error")

        return Response(serializer.data, status=201)

    
    # Wrap common mutating operations to provide clearer error handling and
    # logging for database integrity or unexpected failures.
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            logger.exception("IntegrityError while creating Device")
            raise drf_serializers.ValidationError({"detail": "Database integrity error while creating device."})
        except Exception:
            logger.exception("Unexpected error while creating Device")
            raise APIException("Internal server error")

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except IntegrityError:
            logger.exception("IntegrityError while updating Device")
            raise drf_serializers.ValidationError({"detail": "Database integrity error while updating device."})
        except Exception:
            logger.exception("Unexpected error while updating Device")
            raise APIException("Internal server error")

    def partial_update(self, request, *args, **kwargs):
        try:
            return super().partial_update(request, *args, **kwargs)
        except IntegrityError:
            logger.exception("IntegrityError while partially updating Device")
            raise drf_serializers.ValidationError({"detail": "Database integrity error while updating device."})
        except Exception:
            logger.exception("Unexpected error while partially updating Device")
            raise APIException("Internal server error")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except IntegrityError:
            logger.exception("IntegrityError while deleting Device")
            raise drf_serializers.ValidationError({"detail": "Database integrity error while deleting device."})
        except Exception:
            logger.exception("Unexpected error while deleting Device")
            raise APIException("Internal server error")


# DeviceViewSet exposes standard CRUD for Device and includes a 'logs' member
# action at GET /api/v1/devices/{pk}/logs/. The explicit CreateAPIView and
# separate DeviceLog listing view were redundant and have been removed to keep
# routing centralized under the DeviceViewSet and its router registration.
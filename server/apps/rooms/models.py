"""Rooms app models.

This file intentionally does not duplicate the Room model which is
implemented in `server.apps.devices.models.Room`. It exists so Django
considers `server.apps.rooms` an app module; any app-specific models
should be added here in the future.
"""

from typing import TYPE_CHECKING, Any
import uuid
from django.db import models
from django.utils.timezone import now
from django.apps import apps

class Room(models.Model):
    class Meta:
        db_table = "rooms"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    def device_count(self) -> int:
        # apps.get_model avoids import cycles and works whether Device is in the same module or another one
        Device = apps.get_model('devices', 'Device')
        try:
            return Device.objects.filter(room_id=self.pk).count()
        except Exception:
            # safe fallback: try reverse manager(s) if present
            if hasattr(self, 'devices'):
                try:
                    return self.devices.count()
                except Exception:
                    return 0
            if hasattr(self, 'device_set'):
                try:
                    return self.device_set.count()
                except Exception:
                    return 0
            return 0

    # Type hints for static analyzers (only evaluated during type checking)
    if TYPE_CHECKING:  # pragma: no cover - typing only
        devices: Any
        device_set: Any

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'device_count': int(self.device_count()),
        }
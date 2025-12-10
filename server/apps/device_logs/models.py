"""Device logs models placeholder.

DeviceLog model lives in `server.apps.devices.models.DeviceLog`.
This file exists so devicelogs is recognized as a Django app.
"""

import datetime
import uuid
from django.db import models
from django.utils.timezone import now

class DeviceLog(models.Model):
    class Meta:
        db_table = "device_logs"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=now)

    # Foreign Key - explicitly reference the devices app so Django does not
    # assume the related model lives in this app (device_logs.Device).
    device = models.ForeignKey('devices.Device', related_name='logs', on_delete=models.CASCADE)

    def __str__(self):
        # device_id attribute provided by Django; use device_id to avoid accessing related object
        return f'{self.action} for Device {getattr(self, "device_id", None)}'

    def to_dict(self):
        return {
            'id': self.pk,
            'action': self.action,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime.datetime) else None,
            'device_id': getattr(self, 'device_id', None),
        }


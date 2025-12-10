"""Device categories models placeholder.

DeviceCategory model is defined in `server.apps.devices.models.DeviceCategory`.
This placeholder keeps the app structure in place.
"""

import uuid
from django.db import models

class DeviceCategory(models.Model):
    class Meta:
        db_table = "device_categories"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.pk,
            'name': self.name,
            'icon': self.icon,
        }


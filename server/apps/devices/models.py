"""
TODO: Define Django ORM models corresponding to the Flask SQLAlchemy models
found in `flask-sqlalchemy-server-backup/server/models.py`.

Guidance / checklist:
- Identify each model (Device, Room, Category, User, DeviceLog, etc.) in the Flask backup.
- For each model, create a Django model class with fields mapped to Django field types.
  - Integer/Float -> models.IntegerField / models.FloatField
  - String -> models.CharField (with max_length)
  - Text -> models.TextField
  - Datetime -> models.DateTimeField (use auto_now_add / auto_now as needed)
  - ForeignKey relations -> models.ForeignKey('OtherModel', on_delete=models.CASCADE)
- Add __str__ implementations for readable admin display.
- Add Meta ordering/indexes if necessary.
- Create initial migrations with `python manage.py makemigrations devices` then `migrate`.

Files to update after models exist:
- admin.py: register models for admin UI
- serializers.py: define DRF serializers for API
- views.py: viewsets for CRUD
- urls.py: expose router endpoints

Acceptance criteria:
- All Flask models present and mapped in Django.
- Migrations created and applied locally.
"""


from django.db import models
from django.utils.timezone import now
from django.apps import apps
from typing import Optional, TYPE_CHECKING, Any
import uuid

class Device(models.Model):
    class Meta:
        db_table = "devices"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    mac_address = models.CharField(max_length=17, null=True, blank=True)
    status = models.CharField(max_length=20, default='offline')
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    # Foreign Keys
    # Use explicit app_label.ModelName strings so Django resolves cross-app
    # relations correctly (avoids interpreting 'Room' as 'devices.Room').
    room = models.ForeignKey('rooms.Room', related_name='devices', null=True, blank=True, on_delete=models.SET_NULL)

    category = models.ForeignKey('device_categories.DeviceCategory', related_name='devices', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name} ({self.device_type})'

    def to_dict(self):
        room_obj = getattr(self, 'room', None)
        if room_obj:
            room_data = {'id': room_obj.pk, 'name': room_obj.name}
        else:
            room_data = None

        category_obj = getattr(self, 'category', None)
        if category_obj:
            category_data = {'id': category_obj.pk, 'name': category_obj.name, 'icon': category_obj.icon}
        else:
            category_data = None

        return {
            'id': self.pk,
            'name': self.name,
            'device_type': self.device_type,
            'brand': self.brand,
            'model': self.model,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
            'status': self.status,
            'is_active': self.is_active,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'room': room_data,
            'category': category_data,
        }

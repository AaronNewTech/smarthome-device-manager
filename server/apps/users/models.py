"""Users app models placeholder.

The canonical `User` model lives in `server.apps.devices.models.User`.
This file exists so the users app is a valid Django app and can hold
app-specific models in the future.
"""

import uuid
from django.db import models
from django.utils.timezone import now

class User(models.Model):
    class Meta:
        db_table = "users"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=120, unique=True)
    created_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def to_dict(self):
        return {
            'id': self.pk,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
        }

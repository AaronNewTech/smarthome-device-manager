from rest_framework import serializers
from server.apps.device_logs.models import DeviceLog


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = ('id', 'action', 'old_value', 'new_value', 'timestamp', 'device')
        extra_kwargs = {
            'device': {'read_only': True},
            'timestamp': {'read_only': True},
        }

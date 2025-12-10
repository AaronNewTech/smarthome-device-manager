from rest_framework import serializers
from server.apps.device_categories.models import DeviceCategory


class DeviceCategorySerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DeviceCategory
        fields = ('id', 'name', 'icon', 'device_count')

    def get_device_count(self, obj):
        devices_attr = getattr(obj, 'devices', None)
        if devices_attr is None:
            return 0
        if hasattr(devices_attr, 'count'):
            try:
                return devices_attr.count()
            except Exception:
                return 0
        try:
            return len(devices_attr)
        except Exception:
            return 0

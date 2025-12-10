from rest_framework import serializers


from server.apps.rooms.models import Room


class RoomSerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        # expose primary fields; nested devices are omitted for brevity
        fields = ('id', 'name', 'description', 'created_at', 'device_count')

    def get_device_count(self, obj):
        try:
            return obj.device_count()
        except Exception:
            # safe fallback: if a related manager exists use .count(), otherwise use len()
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

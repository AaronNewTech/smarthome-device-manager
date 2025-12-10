from rest_framework import serializers

from server.apps.device_categories.models import DeviceCategory
from server.apps.devices.models import Device
from server.apps.rooms.models import Room


from server.apps.rooms.serializers import RoomSerializer
from server.apps.device_categories.serializers import DeviceCategorySerializer


class DeviceSerializer(serializers.ModelSerializer):
    # nested read-only representations
    room = RoomSerializer(read_only=True)
    category = DeviceCategorySerializer(read_only=True)

    # accepts PKs for write operations
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), source='room', write_only=True, required=False, allow_null=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=DeviceCategory.objects.all(), source='category', write_only=True, required=False, allow_null=True)

    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "device_type",
            "brand",
            "model",
            "ip_address",
            "mac_address",
            "status",
            "is_active",
            "last_seen",
            "created_at",
            "updated_at",
            "room",
            "category",
            "room_id",
            "category_id",
        )
        read_only_fields = ("id", "created_at", "updated_at", "room", "category")
